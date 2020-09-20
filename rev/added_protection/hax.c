#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>
int main(){
    unsigned char *p = mmap(0,4096,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANON,-1,0);
    memset(p, 0x3c, 4096);
    int f = open("shellcode", O_RDONLY);
    read(f,p,227);
    int (*ret)() = (int(*)()) (p+8);
    ret();
}
