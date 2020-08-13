#!/usr/bin/env python
## -*- coding: utf-8 -*-

from tritondse import *

config = Config()
config.program_argv = [b'./samples/crackme_xor', b'salut']
config.symbolize_stdin = True

pstate  = ProcessState(config)
program = Program('./samples/crackme_xor')
seed    = Seed(b'toto')
se      = SymbolicExecutor(config, pstate, program, seed)

se.run()
