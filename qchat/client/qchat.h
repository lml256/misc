#ifndef QCHAT_H
#define QCHAT_H

#include <QMainWindow>
#include "msggetthread.h"
#include "utils.h"
#include "config.h"


QT_BEGIN_NAMESPACE
namespace Ui { class QChat; }
QT_END_NAMESPACE

class QChat : public QMainWindow
{
    Q_OBJECT

public:
    QChat(QWidget *parent = nullptr);
    ~QChat();

private slots:
    void on_pushButton_clicked();

    void getMsg(QString msg);
    void lossLink();

private:
    Ui::QChat *ui;
    MsgGetThread *thread;
    int fd;
    char buf[BUFSIZE];
};
#endif // QCHAT_H
