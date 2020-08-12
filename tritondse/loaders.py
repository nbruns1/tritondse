#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import lief

from triton                 import *
from tritondse.config       import Config
from tritondse.processState import ProcessState
from tritondse.program      import Program
from tritondse.routines     import *


class ELFLoader(object):
    """
    This class is used to represent the ELF loader mechanism.
    """
    def __init__(self, config : Config, program : Program, pstate : ProcessState):
        self.program = program
        self.pstate  = pstate
        self.config  = config

        # Mapping of the .plt and .got to the Python routines
        self.routines_table = dict()
        self.plt = [
            ['__libc_start_main',       rtn_libc_start_main,        None],
            ['exit',                    rtn_exit,                   None],
            ['puts',                    rtn_puts,                   None],
        ]
        self.gvariables = {
            'stderr': 2,
        }


    def __loading__(self):
        phdrs = self.program.binary.segments
        for phdr in phdrs:
            size  = phdr.physical_size
            vaddr = phdr.virtual_address
            if size:
                logging.debug('Loading 0x%08x - 0x%08x' %(vaddr, vaddr+size))
                self.pstate.tt_ctx.setConcreteMemoryAreaValue(vaddr, phdr.content)


    def __dynamic_relocation__(self, vaddr : int = 0):
        # Initialize our routines table
        for index in range(len(self.plt)):
            self.plt[index][2] = self.pstate.BASE_PLT + index
            self.routines_table.update({self.pstate.BASE_PLT + index: self.plt[index][1]})

        # Initialize the pltgot
        try:
            for rel in self.program.binary.pltgot_relocations:
                symbolName = rel.symbol.name
                symbolRelo = vaddr + rel.address
                for crel in self.plt:
                    if symbolName == crel[0]:
                        logging.debug('Hooking %s at %#x' %(symbolName, symbolRelo))
                        self.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(symbolRelo, CPUSIZE.QWORD), crel[2])
        except:
            logging.error('Something wrong with the pltgot relocations')

        try:
            for rel in self.program.binary.dynamic_relocations:
                symbolName = rel.symbol.name
                symbolRelo = vaddr + rel.address
                for crel in self.plt:
                    if symbolName == crel[0]:
                        logging.debug('Hooking %s at %#x' %(symbolName, symbolRelo))
                        self.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(symbolRelo, CPUSIZE.QWORD), crel[2])
        except:
            logging.error('Something wrong with the dynamic relocations')

        for k, v in self.gvariables.items():
            try:
                vaddr = self.program.binary.binary.get_symbol(k).value
                logging.debug('Hooking %s at %#x' % (k, vaddr))
                self.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(vaddr, self.ctx.getGprSize()), 2)
            except:
                logging.debug('Cannot find the symbol %s' %(k))

        return


    def ld(self):
        self.__loading__()
        self.__dynamic_relocation__()
