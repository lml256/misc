#ifndef _RIO_H
#define _RIO_H

#include <unistd.h>
#include <string.h>
#include <errno.h>

#define RIO_BUFSIZE 8192

typedef struct {
    int     rio_fd;                 /* 描述符 */
    int     rio_cnt;                /* 缓冲区中还未读的字节数 */
    char    *rio_bufptr;            /* 缓冲区中下一个未读的字节 */
    char    rio_buf[RIO_BUFSIZE];   /* 缓冲区 */
} rio_t;

extern ssize_t  rio_readn(int fd, void *buf, size_t n);
extern ssize_t  rio_writen(int fd, void *buf, size_t n);

extern void     rio_readinitb(rio_t *rp, int fd);
extern ssize_t  rio_readlineb(rio_t *rp, void *usrbuf, size_t maxlen);
extern ssize_t  rio_readnb(rio_t *rp, void *usrbuf, size_t n);

#endif // _RIO_H
