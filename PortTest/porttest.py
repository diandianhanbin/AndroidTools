# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com

import requests
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os

f = file("case.json")
testData = json.load(f)
f.close()


def sendData(testData, num):
	payload = {}
	# 从json中获取发送参数
	for x in testData[num]['InputArg'].items():
		payload[x[0]] = x[1]
	with open('leftside.txt', 'a+') as f:
		f.write(testData[num]['TestId'])
		f.write('-')
		f.write(testData[num]['Title'])
		f.write('\n')

	# 发送请求
	data = requests.get(testData[num]['Url'], params=payload)
	r = data.json()

	with open('rightside.txt', 'a+') as rs:
		rs.write('发送数据')
		rs.write('|')
		rs.write('标题:'+testData[num]['Title'])
		rs.write('|')
		rs.write('发送方式:'+testData[num]['Method'])
		rs.write('|')
		rs.write('案例描述:'+testData[num]['Desc'])
		rs.write('|')
		rs.write('发送地址:'+testData[num]['Url'])
		rs.write('|')
		rs.write('发送参数:'+str(payload).decode("unicode-escape").encode("utf-8").replace("u\'","\'"))
		rs.write('|')
		rs.write(testData[num]['TestId'])
		rs.write('\n')

	with open('result.txt', 'a+') as rst:
		rst.write('返回数据')
		rst.write('|')
		for x, y in r.items():
			rst.write(' : '.join([x, y]))
			rst.write('|')
		# 写测试结果
		try:
			if cmp(r, testData[num]['Result']) == 0:
				rst.write('pass')
			else:
				rst.write('fail')
		except Exception:
			rst.write('no except result')
		rst.write('\n')


def getReport():
	"""
	备份测试结果
	注意修改地址和端口
	:return: html源码
	"""
	url = 'http://localhost:1234/porttest/'
	# local_time = time.strftime('%Y%m%d_%H%M%S')
	try:
		web_data = requests.get(url)
	except Exception:
		print "请确认是否已启用端口为1234的Server,或者你修改了端口?程序会自动退出,请启动服务之后自行调用getHtml保存测试结果"
		sys.exit()
	# with open('Report/{}.html'.format(local_time), 'a+') as f:
	# 	f.write(web_data.text)
	getHtml(web_data)
	return web_data.text


def getHtml(web_data):
	local_time = time.strftime('%Y%m%d_%H%M%S')
	with open('Report/{}.html'.format(local_time), 'a+') as f:
		f.write(web_data.text)


if __name__ == '__main__':
	os.system('rm leftside.txt')
	os.system('rm rightside.txt')
	os.system('rm result.txt')
	for x in range(len(testData)):
		sendData(testData, x)
	getReport()