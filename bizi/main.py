#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, uuid, requests
import threading
from lxml import html
from queue import Queue

# 因为当时要爬的网站证书过期，所以忽略了证书验证，但同时也带来了requests的InsecureRequestWarning警告
# 以下忽略requests InsecureRequestWarning警告
requests.packages.urllib3.disable_warnings()


# 伪装请求头
def header(referer):
	headers = {
		'Host': 'h1.ioliu.cn',
		'Pragma': 'no-cache',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Referer': '{}'.format(referer),
	}
	return headers


# 获取图片url
def get_img_url(q: Queue):
	for k in range(1, 101):
		url = 'https://bing.ioliu.cn/?p=%s' % k
		try:
			content = html.fromstring(requests.get(url, verify=False).content)
			page_url = content.xpath('/html/body/div[3]/div/div/img/@src')
		except Exception as e:
			print(e)
			continue
		for i in page_url:
			s = i.replace('400x240', '1920x1080')
			print('获得地址 ' + s)
			q.put(s, True)


def down_image(q: Queue):
	while True:
		url = q.get(True)
		path = 'img/%s.jpg' % uuid.uuid1()
		with open(path, 'wb') as f:
			try:
				f.write(requests.get(url, headers=header(url), timeout=50, verify=False).content)
				print("已下载 %s" % url)
			except Exception as e:
				print(e, " at ", url)


def main():
	if not os.path.exists('img'):
		os.mkdir('img')
	q = Queue(128)
	threads = []
	get_img_url_thread = threading.Thread(target=get_img_url, args=(q,))
	for i in range(12):
		t = threading.Thread(target=down_image, args=(q,))
		threads.append(t)

	get_img_url_thread.start()
	for i in threads:
		i.start()

	get_img_url_thread.join()
	for i in threads:
		i.join()


if __name__ == '__main__':
	main()
