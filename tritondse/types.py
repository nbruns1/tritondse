import sys
from enum    import IntEnum, Enum, auto
from pathlib import Path
from triton  import ARCH, SOLVER
from typing  import Union, TypeVar

# Type representing file either as a file, either as a Path object
PathLike = Union[str, Path]

# Integer representing an address
Addr = int

# Integer representing a relative address
rAddr = int

# Integer representing a value in bits
BitSize = int

# Integer representing a value in bytes
ByteSize = int

Input = bytes
""" Type representing an Input (which is bytes) """

Register = TypeVar('Register')
"""Register object as returned by Triton"""

Registers = TypeVar('Registers')
"""Set of registers as returned by Triton"""

PathConstraint = TypeVar('PathConstraint')
""" PathConstraint object as returned by Triton"""

AstNode = TypeVar('AstNode')
""" SMT logic formula as returned by Triton """

Model = TypeVar('Model')
""" Solver Model as returned by Triton """

Expression = TypeVar('Expression')
""" Symbolic Expression as returned by Triton (SymbolicExpression) """


if sys.version_info.minor >= 8:
    from typing import TypedDict

    class PathBranch(TypedDict):
        """
        Typed dictionnary describing the branch information
        returned by Triton (with getBranchConstraints())
        """
        isTaken: bool
        srcAddr: Addr
        dstAddr: Addr
        constraint: AstNode
else:
    PathBranch = TypeVar('PathBranch')
    """ PathConstraint object as returned by Triton"""


class Architecture(IntEnum):
    """ Common architecture Enum fully compatible with Triton ARCH """
    AARCH64 = ARCH.AARCH64
    ARM32   = ARCH.ARM32
    X86     = ARCH.X86
    X86_64  = ARCH.X86_64


class Solver(IntEnum):
    """ Common Solver Enum fully compatible with Triton ARCH """
    SAT     = SOLVER.SAT
    UNSAT   = SOLVER.UNSAT
    TIMEOUT = SOLVER.TIMEOUT
    UNKNOWN = SOLVER.UNKNOWN


class ConcSymAction(Enum):
    """ Enumeration to represent an action to perform on some
    symbolic data, namely wether or not keep them concrete or
    to symbolize them"""
    CONCRETIZE = auto()
    SYMBOLIZE  = auto()
