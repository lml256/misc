#include "utils.h"
#include "config.h"
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/wait.h>
#include <semaphore.h>

sem_t mutex; // 互斥锁

struct client {
    int fd;
    struct client *next;
};

struct client *client_list;

/* 初始化client链表的头结点 */
void init_list_head(struct client **head, int fd) {
    /* fd为服务器socket fd */
    *head = (struct client *)malloc(sizeof(struct client));
    (*head)->fd = fd;
    (*head)->next = 0;
}

/* 程序强制结束是进行善后处理 */
void end_server(int sig)
{
    struct client *next, *cp;
    cp = client_list;
    do {
        next = cp->next;
        close(cp->fd);
        free(cp);
        cp = next;
    } while (cp != 0);

    fprintf(stdout, "Server has ended\n");

    exit(0);
}

void push_client_list(int);     /* 将客户端的sock加入链表 */
void *listen_msg(void *);       /* 监听客户端的消息 */
void send_msg(char *, size_t);  /* 给客户端发消息 */

int main() {
    int serverfd, client_fd;
    pthread_t tid;

    signal(SIGINT, end_server);

    serverfd = open_listenfd(SERPORT);
    init_list_head(&client_list, serverfd);
    sem_init(&mutex, 0, 1);

    fprintf(stdout, "Server start..., server fd : %d\n", serverfd);

    while (1) {
        client_fd = accept(serverfd, NULL, NULL);
        fprintf(stdout, "Get client connection: fd %d\n", client_fd);
        push_client_list(client_fd);
        if(pthread_create(&tid, NULL, listen_msg, &client_fd) != 0) {
            perror("create thread failed\n");
        }
    }

    return 0;
}


void push_client_list(int fd) {
    struct client *tp, *end;

    tp = (struct client *)malloc(sizeof(struct client));
    tp->fd = fd;
    tp->next = 0;

    sem_wait(&mutex);
    end = client_list;
    while (end->next != 0) {
        end = end->next;
    }
    end->next = tp;
    sem_post(&mutex);
}

void *listen_msg(void *arg) {
    int fd = *((int *)arg);
    struct client *pre, *cp;
    rio_t rio;
    char buf[BUFSIZE];
    int len = 0;

    rio_readinitb(&rio, fd);

    while ((len = rio_readlineb(&rio, buf, BUFSIZE))) {
        fprintf(stdout, "get msg (%d): %s\n", fd, buf);
        sem_wait(&mutex);
        /* 给每一个客户端发消息 */
        send_msg(buf, len);
        sem_post(&mutex);
    }
    close(fd);

    pre = client_list;
    cp = pre->next;
    while (cp != 0) {
        if (cp->fd == fd) {
            pre->next = cp->next;
            free(cp);
            cp = pre->next; /* 指向下一个要处理的client */
        } else {
            pre = cp;
            cp = cp->next;
        }
    }

    printf("Process %d has Exit\n", getpid());
    return NULL;
}

void send_msg(char *buf, size_t n) {
    struct client *pre, *cp;

    pre = client_list;
    cp = client_list->next;
    while (cp != 0) {
        if (rio_writen(cp->fd, buf, n) == -1) {
            /* 如果发送失败，可以认为客户端离线，删除相应的client */
            fprintf(stdout, "Send message to %d failed\n", cp->fd);
            close(cp->fd);
            pre->next = cp->next;
            free(cp);
            cp = pre->next; /* 指向下一个要处理的client */
        } else {
            fprintf(stdout, "Send message to %d successfully\n", cp->fd);
            pre = cp;
            cp = cp->next;
        }
    }
}