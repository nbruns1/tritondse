# Built-in imports
from pathlib import Path
from typing import Union, Generator, Tuple, Optional, Any, List

# third-party imports
import qbinexport
from qbinexport.function import Function, Chunk
from qbinexport.block import Block
from qbinexport.reference import ReferenceType
import networkx
import lief

# local imports
import tritondse.program
from tritondse.coverage import CoverageSingleRun
from tritondse.types import PathLike, Addr, Architecture


class QBinExportProgram(qbinexport.Program):
    def __init__(self, export_file: Union[Path, str], exec_path: Union[Path, str]):
        super(QBinExportProgram, self).__init__(export_file, exec_path)

        self.program = tritondse.program.Program(self.executable.exec_file.as_posix())

    def get_call_graph(self, backedge_on_ret=False) -> networkx.DiGraph:
        """
        Compute the call graph of the program.

        :param backedge_on_ret: if true, add a back edge to represent the "return"
        :return: call graph as a digraph
        """
        g = networkx.DiGraph()
        for fun in self.values():
            g.add_edges_from((fun.start, x.start) for x in fun.calls)
            if backedge_on_ret:  # Add return edge
                g.add_edges_from((x.start, fun.start) for x in fun.calls)
        return g

    @staticmethod
    def get_slice(graph: networkx.DiGraph, frm: Any, to: Any) -> networkx.DiGraph:
        """
        Compute the slice between the two nodes on the given graph.
        The slice is the intersection of reachable node (of ``frm``) and
        ancestors of ``to``. The result is a subgraph of the original graph.

        :param graph: Graph on which to compute the slice
        :param frm: node identifier
        :param to: node identifier
        :return: sub graph
        """
        succs = networkx.descendants(graph, frm)
        preds = networkx.ancestors(graph, to)
        return graph.subgraph(succs.intersection(preds).union({frm, to}))

    def merge(self, coverage: CoverageSingleRun):
        # TODO: To implement
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.export_file.name}  funs:{len(self)}>"

    def get_caller_instructions(self, target: Function) -> List[int]:
        """Get the list of instructions calling `target`
        """

        # Get the first instruction of the target
        first_inst = target.get_instruction(target.start)
        assert first_inst is not None

        # Reference holder
        ref = target.program.references

        caller_instructions = []
        for reference in ref.resolve_inst_instance(first_inst.inst_tuple, ReferenceType.CALL, towards=True):
            block: Block = reference[1]
            found = False
            addr = block.start
            for index, inst in enumerate(block.instructions):
                if index == reference[2]:
                    caller_instructions.append(addr)
                    found = True
                addr += inst.size
            if not found:
                assert False, "Failed to find an instruction"

        return caller_instructions


    # ============== Methods for interroperability with Program object ==============
    @property
    def path(self) -> Path:
        return self.program.path

    @property
    def entry_point(self) -> Addr:
        return self.program.entry_point

    @property
    def architecture(self) -> Architecture:
        return self.program.architecture

    @property
    def endianness(self) -> lief.ENDIANNESS:
        return self.program.endianness

    @property
    def format(self) -> lief.EXE_FORMATS:
        return self.program.format

    @property
    def relocation_enum(self):
        return self.program.relocation_enum

    def memory_segments(self) -> Generator[Tuple[Addr, bytes], None, None]:
        return self.program.memory_segments()

    def imported_functions_relocations(self) -> Generator[Tuple[str, Addr], None, None]:
        return self.program.imported_functions_relocations()

    def imported_variable_symbols_relocations(self) -> Generator[Tuple[str, Addr], None, None]:
        return self.program.imported_variable_symbols_relocations()

    def find_function_addr(self, name: str) -> Optional[Addr]:
        return self.program.find_function_addr(name)

    def find_function_from_addr(self, address: Addr) -> Optional[qbinexport.function.Function]:
        for f in self.values():
            if f.in_func(address):
                return f
