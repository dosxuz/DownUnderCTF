from pwn import *

s = open("shellcode")
#d = open('shell','ab')

for i in s.read().splitlines():
    code = i.strip()
    code = int(code,16) 

    if code < 0x2a:
        code = code - 0x2b
    else:
        code = code - 0x2a

    if (code < 33) and (code < 127):
        print(code)

