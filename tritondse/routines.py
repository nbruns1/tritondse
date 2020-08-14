#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import os
import time

from triton                  import *
from tritondse.enums         import Enums
from tritondse.threadContext import ThreadContext


def rtn_ctype_b_loc(se):
    logging.debug('__ctype_b_loc hooked')

    ctype  = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00"  # must point here
    ctype += b"\x02\x00\x03\x20\x02\x20\x02\x20\x02\x20\x02\x20\x02\x00\x02\x00"
    ctype += b"\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00"
    ctype += b"\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00"
    ctype += b"\x01\x60\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0"
    ctype += b"\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0"
    ctype += b"\x08\xd8\x08\xd8\x08\xd8\x08\xd8\x08\xd8\x08\xd8\x08\xd8\x08\xd8"
    ctype += b"\x08\xd8\x08\xd8\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0"
    ctype += b"\x04\xc0\x08\xd5\x08\xd5\x08\xd5\x08\xd5\x08\xd5\x08\xd5\x08\xc5"
    ctype += b"\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5"
    ctype += b"\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5\x08\xc5"
    ctype += b"\x08\xc5\x08\xc5\x08\xc5\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0"
    ctype += b"\x04\xc0\x08\xd6\x08\xd6\x08\xd6\x08\xd6\x08\xd6\x08\xd6\x08\xc6"
    ctype += b"\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6"
    ctype += b"\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6\x08\xc6"
    ctype += b"\x08\xc6\x08\xc6\x08\xc6\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x02\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ctype += b"\x00\x00\x00\x00\x00\x00\x00\x00"

    size   = se.pstate.tt_ctx.getGprSize()
    ptable = se.pstate.BASE_CTYPE
    table  = (size * 2) + (se.pstate.BASE_CTYPE)
    otable = table + 256

    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(ptable + 0x00, size), otable)
    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(ptable + size, size), 0)

    se.pstate.tt_ctx.setConcreteMemoryAreaValue(table, ctype)

    return Enums.CONCRETIZE, ptable


def rtn_errno_location(se):
    logging.debug('__errno_location hooked')

    errno = 0xdeadbeaf
    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(errno, CPUSIZE.QWORD), 0)

    return Enums.CONCRETIZE, errno


def rtn_libc_start_main(se):
    logging.debug('__libc_start_main hooked')

    # Get arguments
    main = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))

    if se.pstate.tt_ctx.getArchitecture() == ARCH.AARCH64:
        se.pstate.tt_ctx.setConcreteRegisterValue(se.abi.get_pc_register(), main)

    elif se.pstate.tt_ctx.getArchitecture() == ARCH.X86_64:
        # Push the return value to jump into the main() function
        se.pstate.tt_ctx.setConcreteRegisterValue(se.abi.get_sp_register(), se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_sp_register())-CPUSIZE.QWORD)

        ret2main = MemoryAccess(se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_sp_register()), CPUSIZE.QWORD)
        se.pstate.tt_ctx.concretizeMemory(ret2main)
        se.pstate.tt_ctx.setConcreteMemoryValue(ret2main, main)

    # Define concrete value of argc
    argc = len(se.config.program_argv)
    se.pstate.tt_ctx.setConcreteRegisterValue(se.abi.get_arg_register(0), argc)
    logging.debug('argc = %d' %(argc))

    # Define argv
    base = se.pstate.BASE_ARGV
    addrs = list()

    index = 0
    for argv in se.config.program_argv:
        addrs.append(base)
        se.pstate.tt_ctx.setConcreteMemoryAreaValue(base, argv+b'\x00')
        # TODO
        #for indexCell in range(len(argv)):
        #    if se.config.symbolize_argv:
        #        var = se.pstate.tt_ctx.symbolizeMemory(MemoryAccess(base+indexCell, CPUSIZE.BYTE))
        #        var.setAlias('argv[%d][%d]' %(index, indexCell))
        logging.debug('argv[%d] = %s' %(index, repr(se.pstate.tt_ctx.getConcreteMemoryAreaValue(base, len(argv)))))
        base += len(argv)+1
        index += 1

    argv = base
    for addr in addrs:
        se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(base, CPUSIZE.QWORD), addr)
        base += CPUSIZE.QWORD

    # Concrete value
    se.pstate.tt_ctx.setConcreteRegisterValue(se.abi.get_arg_register(1), argv)

    return None


def rtn_stack_chk_fail(se):
    logging.debug('__stack_chk_fail hooked')
    se.pstate.stop = True
    return None


def rtn_exit(se):
    logging.debug('exit hooked')
    arg = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    se.pstate.stop = True
    return Enums.CONCRETIZE, arg


def rtn_free(se):
    logging.debug('free hooked')
    # TODO: MemoryAllocator, save this pointer as freed. Useful for Sanitizers.
    return None


def rtn_fwrite(se):
    logging.debug('fwrite hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    arg1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    arg2 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))
    arg3 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(3))
    size = arg1 * arg2
    data = se.pstate.tt_ctx.getConcreteMemoryAreaValue(arg0, size)

    if arg3 in se.pstate.fd_table:
        if arg3 == 0:
            return Enums.CONCRETIZE, 0
        elif arg3 == 1:
            sys.stdout.buffer.write(data)
            sys.stdout.flush()
        elif arg3 == 2:
            sys.stderr.buffer.write(data)
            sys.stderr.flush()
        else:
            fd = open(se.pstate.fd_table[arg3], 'wb+')
            fd.write(data)
    else:
        return Enums.CONCRETIZE, 0

    # Return value
    return Enums.CONCRETIZE, size


def rtn_gettimeofday(se):
    logging.debug('gettimeofday hooked')

    # Get arguments
    tv = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    tz = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))

    if tv == 0:
        return Enums.CONCRETIZE, ((1 << se.pstate.tt_ctx.getGprBitSize()) - 1)

    t = time.time()
    s = se.pstate.tt_ctx.getGprSize()
    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(tv,   s), int(t))
    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(tv+s, s), int(t * 1000000))

    # Return value
    return Enums.CONCRETIZE, 0


def rtn_malloc(se):
    logging.debug('malloc hooked')

    # Get arguments
    size = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))

    if se.pstate.mallocBase + size > se.pstate.mallocMaxAllocation:
        logging.debug('malloc failed: out of memory')
        sys.exit(-1)

    area = se.pstate.mallocBase
    se.pstate.mallocBase += size

    # TODO: MemoryAllocator, save this pointer as allocated. Useful for Sanitizers.

    # Return value
    return Enums.CONCRETIZE, area


def rtn_memcmp(se):
    logging.debug('memcmp hooked')

    s1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    s2 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    size = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))

    ast = se.pstate.tt_ctx.getAstContext()
    res = ast.bv(0, 64)

    # TODO: What if size is symbolic ?
    for index in range(size):
        cells1 = se.pstate.tt_ctx.getMemoryAst(MemoryAccess(s1+index, 1))
        cells2 = se.pstate.tt_ctx.getMemoryAst(MemoryAccess(s2+index, 1))
        res = res + ast.ite(
                        cells1 == cells2,
                        ast.bv(0, 64),
                        ast.ite(
                            cells1 < cells2,
                            ast.bv(0xffffffffffffffff, 64),
                            ast.bv(1, 64)
                        )
                    )

    # create a new symbolic expression for this summary
    expr = se.pstate.tt_ctx.newSymbolicExpression(res, "memcmp summary")

    return Enums.SYMBOLIZE, expr


def rtn_memcpy(se):
    logging.debug('memcpy hooked')

    dst = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    src = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    cnt = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))

    # TODO: What if cnt is symbolic ?
    for index in range(cnt):
        dmem  = MemoryAccess(dst + index, 1)
        smem  = MemoryAccess(src + index, 1)
        cell = se.pstate.tt_ctx.getMemoryAst(smem)
        expr = se.pstate.tt_ctx.newSymbolicExpression(cell, "memcpy byte")
        se.pstate.tt_ctx.setConcreteMemoryValue(dmem, cell.evaluate())
        se.pstate.tt_ctx.assignSymbolicExpressionToMemory(expr, dmem)

    return Enums.CONCRETIZE, dst


def rtn_memmove(se):
    logging.debug('memmove hooked')

    dst = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    src = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    cnt = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))

    # TODO: What if cnt is symbolic ?
    for index in range(cnt):
        dmem  = MemoryAccess(dst + index, 1)
        smem  = MemoryAccess(src + index, 1)
        cell = se.pstate.tt_ctx.getMemoryAst(smem)
        expr = se.pstate.tt_ctx.newSymbolicExpression(cell, "memmove byte")
        se.pstate.tt_ctx.setConcreteMemoryValue(dmem, cell.evaluate())
        se.pstate.tt_ctx.assignSymbolicExpressionToMemory(expr, dmem)

    return Enums.CONCRETIZE, dst


def rtn_memset(se):
    logging.debug('memset hooked')

    dst = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    src = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    size = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))

    # TODO: What if size is symbolic ?
    for index in range(size):
        dmem = MemoryAccess(dst + index, CPUSIZE.BYTE)
        cell = se.pstate.tt_ctx.getAstContext().extract(7, 0, se.pstate.tt_ctx.getRegisterAst(se.abi.get_arg_register(1)))
        se.pstate.tt_ctx.setConcreteMemoryValue(dmem, cell.evaluate())
        expr = se.pstate.tt_ctx.newSymbolicExpression(cell, "memset byte")
        se.pstate.tt_ctx.assignSymbolicExpressionToMemory(expr, dmem)

    return Enums.CONCRETIZE, dst


def rtn_pthread_create(se):
    logging.debug('pthread_create hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0)) # pthread_t *thread
    arg1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1)) # const pthread_attr_t *attr
    arg2 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2)) # void *(*start_routine) (void *)
    arg3 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(3)) # void *arg

    tid = se.pstate.get_unique_thread_id()
    thread = ThreadContext(se.config, tid)
    thread.save(se.pstate.tt_ctx)

    # Concretize pc
    if se.abi.get_pc_register().getId() in thread.sregs:
        del thread.sregs[se.abi.get_pc_register().getId()]

    # Concretize bp
    if se.abi.get_bp_register().getId() in thread.sregs:
        del thread.sregs[se.abi.get_bp_register().getId()]

    # Concretize sp
    if se.abi.get_sp_register().getId() in thread.sregs:
        del thread.sregs[se.abi.get_sp_register().getId()]

    # Concretize arg0
    if se.abi.get_arg_register(0).getId() in thread.sregs:
        del thread.sregs[se.abi.get_arg_register(0).getId()]

    thread.cregs[se.abi.get_pc_register().getId()] = arg2
    thread.cregs[se.abi.get_arg_register(0).getId()] = arg3
    thread.cregs[se.abi.get_bp_register().getId()] = (se.pstate.BASE_STACK - ((1 << 28) * tid))
    thread.cregs[se.abi.get_sp_register().getId()] = (se.pstate.BASE_STACK - ((1 << 28) * tid))

    se.pstate.threads.update({tid: thread})

    # Save out the thread id
    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize()), tid)

    # Return value
    return Enums.CONCRETIZE, 0


def rtn_pthread_exit(se):
    logging.debug('pthread_exit hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))

    # Kill the thread
    se.pstate.threads[se.pstate.tid].killed = True

    # Return value
    return None


def rtn_pthread_join(se):
    logging.debug('pthread_join hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    arg1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))

    if arg0 in se.pstate.threads:
        se.pstate.threads[se.pstate.tid].joined = arg0
        logging.info('Thread id %d joined thread id %d' % (se.pstate.tid, arg0))
    else:
        se.pstate.threads[se.pstate.tid].joined = None
        logging.debug('Thread id %d already destroyed' % arg0)

    # Return value
    return Enums.CONCRETIZE, 0


def rtn_pthread_mutex_destroy(se):
    logging.debug('pthread_mutex_destroy hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # pthread_mutex_t *restrict mutex
    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize()), se.pstate.PTHREAD_MUTEX_INIT_MAGIC)

    # Return value
    return Enums.CONCRETIZE, 0


def rtn_pthread_mutex_init(se):
    logging.debug('pthread_mutex_init hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # pthread_mutex_t *restrict mutex
    arg1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))  # const pthread_mutexattr_t *restrict attr)

    se.pstate.tt_ctx.setConcreteMemoryValue(MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize()), se.pstate.PTHREAD_MUTEX_INIT_MAGIC)

    # Return value
    return Enums.CONCRETIZE, 0


def rtn_pthread_mutex_lock(se):
    logging.debug('pthread_mutex_lock hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # pthread_mutex_t *mutex
    mem = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())
    mutex = se.pstate.tt_ctx.getConcreteMemoryValue(mem)

    # If the thread has been initialized and unused, define the tid has lock
    if mutex == se.pstate.PTHREAD_MUTEX_INIT_MAGIC:
        logging.debug('mutex unlocked')
        se.pstate.tt_ctx.setConcreteMemoryValue(mem, se.pstate.tid)

    # The mutex is locked and we are not allowed to continue the execution
    elif mutex != se.pstate.tid:
        logging.debug('mutex locked')
        se.pstate.mutex_locked = True

    # Return value
    return Enums.CONCRETIZE, 0


def rtn_pthread_mutex_unlock(se):
    logging.debug('pthread_mutex_unlock hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # pthread_mutex_t *mutex
    mem = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())

    se.pstate.tt_ctx.setConcreteMemoryValue(mem, se.pstate.PTHREAD_MUTEX_INIT_MAGIC)

    # Return value
    return Enums.CONCRETIZE, 0


def rtn_puts(se):
    logging.debug('puts hooked')

    # Get arguments
    arg0 = se.abi.get_string_argument(0)
    sys.stdout.write(arg0 + '\n')
    sys.stdout.flush()

    # Return value
    return Enums.CONCRETIZE, len(arg0) + 1


def rtn_read(se):
    logging.debug('read hooked')

    # Get arguments
    fd   = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    buff = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    size = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))
    minsize = min(len(se.seed.content), size)

    if fd == 0 and se.config.symbolize_stdin:
        for index in range(minsize):
            var = se.pstate.tt_ctx.symbolizeMemory(MemoryAccess(buff + index, CPUSIZE.BYTE))
            var.setComment('stdin[%d]' % index)
            if se.seed:
                try:
                    se.pstate.tt_ctx.setConcreteVariableValue(var, se.seed.content[index])
                except:
                    pass
        logging.debug('stdin = %s' % (repr(se.pstate.tt_ctx.getConcreteMemoryAreaValue(buff, minsize))))
        # TODO: Could return the read value as a symbolic one
        return Enums.CONCRETIZE, minsize

    if fd in se.pstate.fd_table:
        if fd == 0:
            data = os.read(0, size)
        else:
            data = os.read(se.pstate.fd_table[fd], size)

        se.pstate.tt_ctx.setConcreteMemoryAreaValue(buff, data)

    else:
        return Enums.CONCRETIZE, 0

    # Return value
    return Enums.CONCRETIZE, len(data)


def rtn_sem_destroy(se):
    logging.debug('sem_destroy hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_ret_register(0))  # sem_t *sem
    mem = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())

    # Destroy the semaphore with the value
    se.pstate.tt_ctx.setConcreteMemoryValue(mem, 0)

    # Return success
    return Enums.CONCRETIZE, 0


def rtn_sem_getvalue(se):
    logging.debug('sem_getvalue hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # sem_t *sem
    arg1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))  # int *sval
    memIn = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())
    memOut = MemoryAccess(arg1, se.pstate.tt_ctx.getGprSize())
    value = se.pstate.tt_ctx.getConcreteMemoryValue(memIn)

    # Set the semaphore's value into the output
    se.pstate.tt_ctx.setConcreteMemoryValue(memOut, value)

    # Return success
    return Enums.CONCRETIZE, 0


def rtn_sem_init(se):
    logging.debug('sem_init hooked')

    # Get arguments
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # sem_t *sem
    arg1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))  # int pshared
    arg2 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))  # unsigned int value
    mem = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())

    # Init the semaphore with the value
    se.pstate.tt_ctx.setConcreteMemoryValue(mem, arg2)

    # Return success
    return Enums.CONCRETIZE, 0


def rtn_sem_post(se):
    logging.debug('sem_post hooked')

    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # sem_t *sem
    mem  = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())

    # increments (unlocks) the semaphore pointed to by sem
    value = se.pstate.tt_ctx.getConcreteMemoryValue(mem)

    se.pstate.tt_ctx.setConcreteMemoryValue(mem, value + 1)

    # Return success
    return Enums.CONCRETIZE, 0


def rtn_sem_timedwait(se):
    logging.debug('sem_timedwait hooked')

    arg0  = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # sem_t *sem
    arg0m = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())
    arg1  = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))  # const struct timespec *abs_timeout
    arg1m = MemoryAccess(arg1, se.pstate.tt_ctx.getGprSize())

    # sem_timedwait() is the same as sem_wait(), except that abs_timeout specifies a limit
    # on the amount of time that the call should block if the decrement cannot be immediately
    # performed. The abs_timeout argument points to a structure that specifies an absolute
    # timeout in seconds and nanoseconds since the Epoch, 1970-01-01 00:00:00 +0000 (UTC).
    # This structure is defined as follows:
    #
    #     struct timespec {
    #         time_t tv_sec;      /* Seconds */
    #         long   tv_nsec;     /* Nanoseconds [0 .. 999999999] */
    #     };
    #
    # If the timeout has already expired by the time of the call, and the semaphore could not be
    # locked immediately, then sem_timedwait() fails with a timeout error (errno set to ETIMEDOUT).
    #
    # If  the operation can be performed immediately, then sem_timedwait() never fails with a
    # timeout error, regardless of the value of abs_timeout.  Furthermore, the validity of
    # abs_timeout is not checked in this case.

    # TODO: Take into account the abs_timeout argument
    value = se.pstate.tt_ctx.getConcreteMemoryValue(arg0m)
    if value > 0:
        logging.debug('semaphore still not locked')
        se.pstate.tt_ctx.setConcreteMemoryValue(arg0m, value - 1)
    else:
        logging.debug('semaphore locked')
        se.pstate.semaphore_locked = True

    # Return success
    return Enums.CONCRETIZE, 0


def rtn_sem_trywait(se):
    logging.debug('sem_trywait hooked')

    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # sem_t *sem
    mem = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())

    # sem_trywait()  is  the  same as sem_wait(), except that if the decrement
    # cannot be immediately performed, then call returns an error (errno set to
    # EAGAIN) instead of blocking.
    value = se.pstate.tt_ctx.getConcreteMemoryValue(mem)
    if value > 0:
        logging.debug('semaphore still not locked')
        se.pstate.tt_ctx.setConcreteMemoryValue(mem, value - 1)
    else:
        logging.debug('semaphore locked')
        return Enums.CONCRETIZE, ((1 << se.pstate.tt_ctx.getGprBitSize()) - 1)

    # Return success
    return Enums.CONCRETIZE, 0


def rtn_sem_wait(se):
    logging.debug('sem_wait hooked')

    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))  # sem_t *sem
    mem = MemoryAccess(arg0, se.pstate.tt_ctx.getGprSize())

    # decrements (locks) the semaphore pointed to by sem. If the semaphore's value
    # is greater than zero, then the decrement proceeds, and the function returns,
    # immediately. If the semaphore currently has the value zero, then the call blocks
    # until either it becomes possible to perform the decrement (i.e., the semaphore
    # value rises above zero).
    value = se.pstate.tt_ctx.getConcreteMemoryValue(mem)
    if value > 0:
        logging.debug('semaphore still not locked')
        se.pstate.tt_ctx.setConcreteMemoryValue(mem, value - 1)
    else:
        logging.debug('semaphore locked')
        se.pstate.semaphore_locked = True

    # Return success
    return Enums.CONCRETIZE, 0


def rtn_sprintf(se):
    logging.debug('sprintf hooked')

    # Get arguments
    buf  = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    arg0 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    arg1 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))
    arg2 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(3))
    arg3 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(4))
    arg4 = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(5))

    arg0f = se.abi.get_format_string(arg0)
    nbArgs = arg0f.count("{")
    args = se.abi.get_format_arguments(arg0, [arg1, arg2, arg3, arg4][:nbArgs])
    s = arg0f.format(*args)

    index = 0
    for c in s:
        se.pstate.tt_ctx.concretizeMemory(buf + index)
        se.pstate.tt_ctx.setConcreteMemoryValue(buf + index, ord(c))
        index += 1

    return Enums.CONCRETIZE, len(s)


def rtn_strlen(se):
    logging.debug('strlen hooked')

    # Get arguments
    s = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))

    ast = se.pstate.tt_ctx.getAstContext()
    def rec(res, s, deep, maxdeep):
        if deep == maxdeep:
            return res
        cell = se.pstate.tt_ctx.getMemoryAst(MemoryAccess(s + deep, 1))
        res  = ast.ite(cell == 0x00, ast.bv(deep, 64), rec(res, s, deep+1, maxdeep))
        return res

    sze = len(se.abi.get_memory_string(s))
    res = ast.bv(sze, 64)
    res = rec(res, s, 0, sze)

    # create a new symbolic expression for this summary
    expr = se.pstate.tt_ctx.newSymbolicExpression(res, "strlen summary")

    return Enums.SYMBOLIZE, expr


def rtn_strncpy(se):
    logging.debug('strncpy hooked')

    dst = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(0))
    src = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(1))
    cnt = se.pstate.tt_ctx.getConcreteRegisterValue(se.abi.get_arg_register(2))
    # TODO: What if the cnt is symbolic ?
    for index in range(cnt):
        dmem = MemoryAccess(dst + index, 1)
        smem = MemoryAccess(src + index, 1)
        cell = se.pstate.tt_ctx.getMemoryAst(smem)
        expr = se.pstate.tt_ctx.newSymbolicExpression(cell, "strncpy byte")
        se.pstate.tt_ctx.setConcreteMemoryValue(dmem, cell.evaluate())
        se.pstate.tt_ctx.assignSymbolicExpressionToMemory(expr, dmem)
        if cell.evaluate() == 0:
            break

    return Enums.CONCRETIZE, dst
