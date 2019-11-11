#ifndef MSGGETTHREAD_H
#define MSGGETTHREAD_H

#include <QThread>
#include "utils.h"


class MsgGetThread: public QThread
{
    Q_OBJECT
public:
    MsgGetThread(int fd);
    ~MsgGetThread();

protected:
    void run();

signals:
    void getMsg(QString msg);
    void lossLink();

private:
    int fd;
};

#endif // MSGGETTHREAD_H
