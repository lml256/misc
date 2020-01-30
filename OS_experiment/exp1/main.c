//
// Created by lml on 7/2/19.
//
#include <sys/shm.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <semaphore.h>

#define SHM_MODE 0600  /*用户读 用户写*/
#define SEM_MODE 0600

sem_t *empty, *full, *mutex;  /* 信号量ID */
int *array, *set, *get, *product;  /* 缓冲区 生产者指针 消费者指针 */
int *k_array, *q_array;  /* 每个生产者生产的产品数  每个消费者消费的产品数 */
int ind, b; /* 第几个生产者或消费者  缓冲区大小 */

void producer() {
    int num = k_array[ind];
    printf("Producer process %d begin\n", getpid());
    for (int i = 0; i < num; i++) {
        printf("Producer process %d block\n", getpid());
//        sleep(1);
        sem_wait(empty);
        sem_wait(mutex);
        printf("Producer process %d wake up\n", getpid());
        array[(*set) % b] = *product;
        printf("Producer process %d put the product %d into buffer\n", getpid(), *product);
        (*set)++;
        (*product)++;
        sem_post(mutex);
        sem_post(full);
    }
}

void customer() {
    int num = q_array[ind];
    printf("Customer process %d begin\n", getpid());
    for (int i = 0; i < num; i++) {
        printf("Customer process %d block\n", getpid());
        sem_wait(full);
        sem_wait(mutex);
        printf("Customer process %d wake up\n", getpid());
        printf("Customer process %d take the product %d from buffer\n", getpid(), array[(*get) % b]);
        (*get)++;
        sem_post(mutex);
        sem_post(empty);
    }
}


int main() {
    int type = 0; /*进程属性 0-主进程 1-生产者进程 2-消费者进程*/
    pid_t pid;

    int producer_sum, customer_sum;
    printf("Enter the buffer size: ");
    scanf("%d", &b);
    printf("Enter the number of producer: ");
    scanf("%d", &producer_sum);
    printf("Enter the number of customer: ");
    scanf("%d", &customer_sum);

    /*初始化共享主存*/
    int array_id, set_id, get_id, product_id, k_array_id, q_array_id;
    array_id = shmget(IPC_PRIVATE, sizeof(int) * b, SHM_MODE);
    set_id = shmget(IPC_PRIVATE, sizeof(int), SHM_MODE);
    get_id = shmget(IPC_PRIVATE, sizeof(int), SHM_MODE);
    product_id = shmget(IPC_PRIVATE, sizeof(int), SHM_MODE);
    k_array_id = shmget(IPC_PRIVATE, sizeof(int) * producer_sum, SHM_MODE);
    q_array_id = shmget(IPC_PRIVATE, sizeof(int) * customer_sum, SHM_MODE);

    if ((array = (int *) shmat(array_id, NULL, 0)) == (void *) -1) perror("error");
    if ((set = (int *) shmat(set_id, NULL, 0)) == (void *) -1) perror("error");
    if ((get = (int *) shmat(get_id, NULL, 0)) == (void *) -1) perror("error");
    if ((product = (int *) shmat(product_id, NULL, 0)) == (void *) -1) perror("error");
    if ((k_array = (int *) shmat(k_array_id, NULL, 0)) == (void *) -1) perror("error");
    if ((q_array = (int *) shmat(q_array_id, NULL, 0)) == (void *) -1) perror("error");
    *product = *set = *get = 0;

    printf("Enter the number of products each producer wants to produce:\n");
    for (int i = 0; i < producer_sum; i++) {
        scanf("%d", k_array + i);
    }
    printf("Enter the number of products each customer wants to take:\n");
    for (int i = 0; i < customer_sum; i++) {
        scanf("%d", q_array + i);
    }

    /*初始化信号量*/
    empty = sem_open("/empty", O_CREAT | O_EXCL, SEM_MODE, b);
    full = sem_open("/full", O_CREAT | O_EXCL, SEM_MODE, 0);
    mutex = sem_open("/mutex", O_CREAT | O_EXCL, SEM_MODE, 1);

    /*创建进程*/
    for (int i = 0; i < producer_sum; i++) {
        pid = fork();
        if (pid == -1) perror("fork");
        if (pid == 0) {
            ind = i;
            type = 1;
            break;
        }
    }

    if (type == 0) {
        for (int i = 0; i < customer_sum; i++) {
            pid = fork();
            if (pid == -1) perror("fork");
            if (pid == 0) {
                ind = i;
                type = 2;
                break;
            }
        }
    }

    if (type == 0) {
        while (wait(NULL) != -1) {
            /*等待所有进程退出*/
        }
        /*删除信号量*/
        sem_unlink("/empty");
        sem_unlink("/full");
        sem_unlink("/mutex");

        /*释放共享主存*/
        if (shmctl(array_id, IPC_RMID, 0) < 0) perror("shmctl error");
        if (shmctl(set_id, IPC_RMID, 0) < 0) perror("shmctl error");
        if (shmctl(get_id, IPC_RMID, 0) < 0) perror("shmctl error");
        if (shmctl(product_id, IPC_RMID, 0) < 0) perror("shmctl error");
        if (shmctl(k_array_id, IPC_RMID, 0) < 0) perror("shmctl error");
        if (shmctl(q_array_id, IPC_RMID, 0) < 0) perror("shmctl error");

        printf("Main Process Exit\n");
        return 0;
    } else if (type == 1) {
        producer();
        printf("Producer process %d exit\n", getpid());
    } else {
        customer();
        printf("Customer process %d exit\n", getpid());
    }

    /*断开共享主存*/
    shmdt(array);
    shmdt(set);
    shmdt(get);
    shmdt(product);
    shmdt(k_array);
    shmdt(q_array);
    return 0;
}

