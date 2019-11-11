#include "msggetthread.h"
#include <QDebug>

MsgGetThread::MsgGetThread(int fd)
{
    this->fd = fd;
}

void MsgGetThread::run()
{
    rio_t rio;
    char buf[BUFSIZE];
    int len = 0;

    rio_readinitb(&rio, this->fd);

    /* 不断等待读入一行消息，如果出错则退出线程 */
    while(true) {
        len = rio_readlineb(&rio, buf, BUFSIZE);
        if(len <= 0) {
            qDebug() << "MsgGetThread: rio_readlineb error";
            break;
        }
        buf[len] = 0;
        QByteArray qba(buf);
        QString msg = QString::fromLocal8Bit(qba);
        /* 取得消息后，发出getMsg信号 */
        emit getMsg(msg);
    }
    /* 异常退出，发出断开连接信号 */
    emit lossLink();
}

MsgGetThread::~MsgGetThread()
{

}
