# built-ins
import sys
import time
import logging

# third-party
from triton import TritonContext, MemoryAccess

# local imports
from tritondse.thread_context import ThreadContext
from tritondse.config         import Config
from tritondse.program        import Program
from tritondse.types import Architecture, Addr, Bytes


class ProcessState(object):
    """
    This class is used to represent the state of a process.
    """
    def __init__(self, config: Config):
        # Memory mapping
        self.BASE_PLT   = 0x01000000
        self.BASE_ARGV  = 0x02000000
        self.BASE_ALLOC = 0x03000000
        self.BASE_STACK = 0xefffffff
        self.BASE_LIBC  = 0x04000000
        self.BASE_CTYPE = 0x05000000
        self.START_MAP  = 0x01000000
        self.END_MAP    = 0xf0000000

        # The Triton's context
        self.tt_ctx = TritonContext()

        # Used to define that the process must exist
        self.stop = False

        # Signals table used by raise(), signal(), etc.
        self.signals_table = dict()

        # File descriptors table used by fopen(), fprintf(), etc.
        self.fd_table = {
            0: sys.stdin,
            1: sys.stdout,
            2: sys.stderr,
        }
        # Unique file id incrementation
        self.fd_id = len(self.fd_table)

        # Allocation information used by malloc()
        self.mallocMaxAllocation = 0x03ffffff
        self.mallocBase = self.BASE_ALLOC

        # Unique thread id incrementation
        self.utid = 0

        # Current thread id
        self.tid = self.utid

        # Threads contexts
        self.threads = {
            self.utid: ThreadContext(config, self.tid)
        }

        # Thread mutext init magic number
        self.PTHREAD_MUTEX_INIT_MAGIC = 0xdead

        # Mutex and semaphore
        self.mutex_locked = False
        self.semaphore_locked = False

        # The time when the ProcessState is instancied.
        # It's used to provide a deterministic behavior when calling functions
        # like gettimeofday(), clock_gettime(), etc.
        self.time = time.time()


    def get_unique_thread_id(self):
        self.utid += 1
        return self.utid


    def get_unique_file_id(self):
        self.fd_id += 1
        return self.fd_id

    @property
    def architecture(self) -> Architecture:
        """ Return architecture of the current process state """
        return Architecture(self.tt_ctx.getArchitecture())

    @architecture.setter
    def architecture(self, arch: Architecture) -> None:
        """
        Set the architecture of the process state.
        Internal set it in the TritonContext
        """
        self.tt_ctx.setArchitecture(arch)

    @property
    def addr_size(self) -> Bytes:
        """ Size of an address in bytes """
        return self.tt_ctx.getGprSize()

    def load_program(self, p: Program) -> None:
        """
        Load the given program in the process state memory
        :param p: Program to load in the process memory
        :return: True on whether loading succeeded or not
        """
        # Load memory areas in memory
        for vaddr, data in p.memory_segments():
            logging.debug(f"Loading {vaddr:#08x} - {vaddr+len(data):#08x}")
            self.tt_ctx.setConcreteMemoryAreaValue(vaddr, data)

    def write_memory(self, addr: Addr, size: Bytes, data: int) -> None:
        """
        Write in the process memory the given data of the given size at
        a specific address.
        :param addr: address where to write data
        :param size: size of data to write in bytes
        :param data: data to write represented as an integer
        :return: None

        .. todo:: Adding a parameter to specify endianess if needed
        """
        self.tt_ctx.setConcreteMemoryValue(MemoryAccess(addr, size), data)
