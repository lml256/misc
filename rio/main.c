#include "rio.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define MAXLEN 1024

int main()
{
    int fd, n;
    char buf[MAXLEN];
    char* s = "hello";

    /* without buf */
    fd = open("foo.txt", O_RDWR, 0);
    while ((n = rio_readn(fd, buf, 1)) > 0) {
        buf[1] = 0;
        printf("%s\n", buf);
    }

    rio_writen(fd, s, strlen(s));
    close(fd);

    puts("=========");

    /* with buf */
    fd = open("foo.txt", O_RDWR, 0);

    rio_t rio;

    rio_readinitb(&rio, fd);
    while ((n = rio_readlineb(&rio, buf, MAXLEN)) > 0) {
        printf("%s\n", buf);
    }
    close(fd);
    return 0;
}
