from __future__ import annotations

# built-in imports
from collections import namedtuple
from pathlib import Path
from typing import Optional, Generator, Tuple, Dict
import logging

# local imports
from tritondse.types import Addr, Architecture, Platform, ArchMode, PathLike, Perm
from tritondse.arch import ARCHS


LoadableSegment = namedtuple('LoadableSegment', 'address perms content')


class Loader(object):
    """
    This class describes how to load the target program in memory.
    """

    @property
    def name(self) -> str:
        """
        Name of the loader and target being loaded.

        :return: str of the loader name
        """
        raise NotImplementedError()

    @property
    def entry_point(self) -> Addr:
        """
        Program entrypoint address as defined in the binary headers

        :rtype: :py:obj:`tritondse.types.Addr`
        """
        raise NotImplementedError()

    @property
    def architecture(self) -> Architecture:
        """
        Architecture enum representing program architecture.

        :rtype: Architecture
        """
        raise NotImplementedError()

    @property
    def arch_mode(self) -> Optional[ArchMode]:
        """
        ArchMode enum representing the starting mode (e.g Thumb for ARM).
        if None, the default mode of the architecture will be used.

        :rtype: Optional[ArchMode]
        """
        return None

    @property
    def platform(self) -> Optional[Platform]:
        """
        Platform of the binary.

        :return: Platform
        """
        return None

    def memory_segments(self) -> Generator[LoadableSegment, None, None]:
        """
        Iterate over all memory segments of the program as loaded in memory.

        :return: Generator of tuples addrs and content
        :raise NotImplementedError: if the binary format cannot be loaded
        """
        raise NotImplementedError()


    @property
    def cpustate(self) -> Dict[str, int]:
        """
        Provide the initial cpu state in the forma of a dictionary of
        {"register_name" : register_value}
        """
        return {}


    def imported_functions_relocations(self) -> Generator[Tuple[str, Addr], None, None]:
        """
        Iterate over all imported functions by the program. This function
        is a generator of tuples associating the function and its relocation
        address in the binary.

        :return: Generator of tuples function name and relocation address
        """
        yield from ()

    def imported_variable_symbols_relocations(self) -> Generator[Tuple[str, Addr], None, None]:
        """
        Iterate over all imported variable symbols. Yield for each of them the name and
        the relocation address in the binary.

        :return: Generator of tuples with symbol name, relocation address
        """
        yield from ()

    def find_function_addr(self, name: str) -> Optional[Addr]:
        """
        Search for the function name in fonctions of the binary.

        :param name: Function name
        :type name: str
        :return: Address of function if found
        :rtype: Addr
        """
        return None


class MonolithicLoader(Loader):
    """
    Monolithic loader. It helps loading raw firmware at a given address
    in DSE memory space, with the various attributes like architecture etc.
    """

    def __init__(self, path: PathLike, architecture: Architecture, load_address: Addr, cpustate: Dict[str, int] = None,
                 vmmap: Dict[Addr, bytes] = None, set_thumb: bool = False, platform: Platform = None):

        super(MonolithicLoader, self).__init__()
        self.path: Path = Path(path)  #: Binary file path
        if not self.path.is_file():
            raise FileNotFoundError(f"file {path} not found (or not a file)")

        self.bin_path = path
        self.load_address = load_address
        self._architecture = architecture
        self._platform = platform if platform else None
        self._cpustate = cpustate if cpustate else {}
        self.vmmap = vmmap if vmmap else None
        self._arch_mode = ArchMode.THUMB if set_thumb else None
        if self._platform and (self._architecture, self._platform) in ARCHS:
            self._archinfo = ARCHS[(self._architecture, self._platform)]
        elif self._architecture in ARCHS:
            self._archinfo = ARCHS[self._architecture]
        else: 
            logging.error("Unknown architecture")
            assert False

    @property
    def name(self) -> str:
        """ Name of the loader"""
        return f"Monolithic({self.path})"

    @property
    def architecture(self) -> Architecture:
        """
        Architecture enum representing program architecture.

        :rtype: Architecture
        """
        return self._architecture


    @property
    def arch_mode(self) -> ArchMode:
        """
        ArchMode enum representing the starting mode (e.g Thumb for ARM).

        :rtype: ArchMode
        """
        return self._arch_mode


    @property
    def entry_point(self) -> Addr:
        """
        Program entrypoint address as defined in the binary headers

        :rtype: :py:obj:`tritondse.types.Addr`
        """
        return self.cpustate[self._archinfo.pc_reg]


    def memory_segments(self) -> Generator[LoadableSegment, None, None]:
        """
        In the case of a monolithic firmware, there is a single segment.
        The generator returns a single tuple with the load address and the content.

        :return: Generator of tuples addrs and content
        """
        with open(self.bin_path, "rb") as fd: 
            data = fd.read()
        yield LoadableSegment(self.load_address, Perm.R | Perm.W | Perm.X, data)

        if self.vmmap:
            for (addr, buffer) in self.vmmap.items():
                yield LoadableSegment(addr, Perm.R | Perm.W | Perm.X, buffer)

    @property
    def cpustate(self) -> Dict[str, int]:
        """
        Provide the initial cpu state in the format of a dictionary of
        {"register_name" : register_value}
        """
        return self._cpustate

    @property
    def platform(self) -> Optional[Platform]:
        """
        Platform of the binary.

        :return: Platform
        """
        return self._platform
