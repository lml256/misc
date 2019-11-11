#include "qchat.h"
#include "ui_qchat.h"
#include <QDebug>
#include <QByteArray>
#include <QMessageBox>

QChat::QChat(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::QChat)
{

    /* 打开一个客户端的连接 */
    this->fd = open_clientfd(SERHOST, SERPORT);

    if(this->fd == -1) {
        /* 如果无法连接到服务器，则显示错误消息并退出 */
        QMessageBox msgBox;
        msgBox.setText("Server connect failed");
        msgBox.exec();
        exit(-1);
    }

    /* 创建一个新的线程，用于接受消息 */
    thread = new MsgGetThread(this->fd);

    /* 绑定信号和槽 */
    connect(thread, &MsgGetThread::getMsg, this, &QChat::getMsg);
    connect(thread, &MsgGetThread::lossLink, this, &QChat::lossLink);

    /* 启动线程 */
    thread->start();

    ui->setupUi(this);
}


void QChat::getMsg(QString msg)
{
    /* 收到消息后，将消息追加到展示框 */
    this->ui->MsgShow->append(msg);
    this->ui->MsgSend->moveCursor(QTextCursor::End);
    qDebug() << "get msg: " << msg;
}

void QChat::lossLink()
{
    /* 失去连接后，显示消息 */
    QMessageBox msgBox;
    msgBox.setText("Link lossed");
    msgBox.exec();
}

QChat::~QChat()
{
    /* 退出时，销毁子线程 */
    this->thread->terminate();
    this->thread->wait();
    qDebug() << "MsgGetThread exit";
    delete ui;
    delete thread;
}


void QChat::on_pushButton_clicked()
{
    /* 获取昵称 */
    QString username = this->ui->UsrName->text();
    /* 获取消息 */
    QString msg = this->ui->MsgSend->toPlainText();
    /* 将昵称和消息格式化后转换为字节数组 */
    QByteArray mbt = (username + ":  " + msg).toLocal8Bit();
    char *mc = mbt.data();
    int len = strlen(mc);
    memcpy(buf, mc, len);
    buf[len++] = '\n';
    buf[len] = 0;
    /* 发送消息 */
    if(rio_writen(this->fd, buf, len) < 0) {
        QMessageBox msgBox;
        msgBox.setText("Send failed");
        msgBox.exec();
    } else {
       this->ui->MsgSend->clear();
        qDebug() << "Send successfully";
    }
}
