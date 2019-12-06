#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, threading, sys

flag = False


def resave(sock):
	global flag
	while True:
		data = sock.recv(1024).decode("utf-8")
		if data == "exit":
			flag = True
			break
		print(data)


def sendMessage(sock):
	global flag
	while True:
		data = input()
		if flag:
			break
		sock.send(bytes(data, encoding="utf-8"))
		if data == "exit":
			break


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('39.106.15.221', 3933))

	res = threading.Thread(target=resave, args=(s,))
	sen = threading.Thread(target=sendMessage, args=(s,))

	res.start()
	sen.start()

	res.join()
	sen.join()
	s.close()


if __name__ == '__main__':
	main()
