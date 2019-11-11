#ifndef UTILS_H
#define UTILS_H

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/unistd.h>
#include <errno.h>

#define LISTENQ 20

int open_clientfd(char *hostname, char *port);

#define RIO_BUFSIZE 8192
#define BUFSIZE 8192

typedef struct {
    int     rio_fd;                 /* 描述符 */
    int     rio_cnt;                /* 缓冲区中还未读的字节数 */
    char    *rio_bufptr;            /* 缓冲区中下一个未读的字节 */
    char    rio_buf[RIO_BUFSIZE];   /* 缓冲区 */
} rio_t;

extern ssize_t  rio_writen(int fd, void *buf, size_t n);

extern void     rio_readinitb(rio_t *rp, int fd);
extern ssize_t  rio_readlineb(rio_t *rp, void *usrbuf, size_t maxlen);

#endif // UTILS_H
