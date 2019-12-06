#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, time, datetime, threading

host = []

user = {"Liu Mingliang": "12345", "Chen Qinglong": "12345", "Tian Jilin": "12345"}


def login(sock: socket):
	sock.send(("请输入用户名：").encode("utf-8"))
	username = sock.recv(1024).decode("utf-8")
	sock.send(("请输入密码").encode("utf-8"))
	password = sock.recv(1024).decode("utf-8")
	if user.get(username):
		if user[username] == password:
			for hs in host:
				hs.send(("%s 上线" % username).encode('utf-8'))
			return username, True

	sock.send(("用户名或密码错误, 拒接访问, 回车退出").encode("utf-8"))
	sock.send(("exit").encode("utf-8"))
	return "", False



def tcplink(sock: socket, addr: tuple) -> object:
	time1 = datetime.datetime.now()
	time1_str = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')
	with open("server.log", "a") as f:
		print("%s" % time1_str, file=f)
		print("Accept new connection from %s..." % addr[0], file=f)

	username, flag = login(sock)
	if flag:
		sock.send(b"Welcome!")
		while True:
			try:
				data = sock.recv(1024)
				time.sleep(0.1)
				if data.decode('utf-8') == 'exit':
					for hs in host:
						hs.send(("%s 下线\n" % username).encode('utf-8'))
					sock.send(("%s" % data.decode("utf-8")).encode("utf-8"))
					break
				time1 = datetime.datetime.now()
				time1_str = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')
				for hs in host:
					hs.send(("%s:\n%s 说: %s\n" % (time1_str, username, data.decode('utf-8'))).encode('utf-8'))
			except ConnectionResetError as e:
				with open("server.log", "a") as f:
					for hs in host:
						if hs is not sock:
							hs.send(("%s 下线\n" % username).encode('utf-8'))
					print("客户机断线", file=f)
				break

	# 关闭连接，退出进程
	sock.close()
	time1 = datetime.datetime.now()
	time1_str = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')
	with open("server.log", "a") as f:
		print("%s" % time1_str, file=f)
		print("Connection from %s closed." % addr[0], file=f)
	host.remove(sock)


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('127.0.0.1', 3933))

	s.listen(5)
	print("已开启服务...")

	while True:
		sock, addr = s.accept()
		t = threading.Thread(target=tcplink, args=(sock, addr))
		t.start()
		host.append(sock)
		with open("server.log", "a") as f:
			print("now, have %d host" % len(host), file=f)


if "__main__" == __name__:
	main()
