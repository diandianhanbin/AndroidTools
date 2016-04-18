# ecoding=utf-8
import os
import time
import monkey
import common
import ConfigParser

__author__ = "Sven_Weng"


class Adb:
	def __init__(self):
		self.mk = monkey.Monkey()
		self.cm = common.Common()
		self.cf = ConfigParser.ConfigParser()

	def get_devices(self):
		"""
		获取设备名称
		:return:设备名称
		"""
		a = os.popen('adb devices')
		devices = a.readlines()
		spl = devices[1].find('	')
		devices_name = devices[1][:spl]
		if devices_name == '':
			return "请确认设备是否连接"
		else:
			return devices_name

	def get_monkey_id(self):
		"""
		获取monkey进程ID
		:return:monkey进程id
		"""
		if self.get_devices():
			a = os.popen('adb shell ps | grep monkey')
			try:
				monkey_id = a.read().split(' ')[5]
				print "进程为{} 的Monkey已停止".format(monkey_id)
			except Exception:
				monkey_id = ''
			return monkey_id
		else:
			print "设备未连接"

	def stop_monkey(self, entry):
		"""
		停止monkey
		:param monkey_id:monkey的进程号
		:return:None
		"""
		monkey_id = self.get_monkey_id()
		if monkey_id != '请确认你的设备是否连接':
			os.system('adb shell kill {}'.format(monkey_id))
			self.cm.set_text(entry, "进程为{} 的Monkey已停止".format(monkey_id))
		else:
			print "设备未连接"

	def get_cpuinfo(self, package_name, url):
		"""
		往cpuinfo文件夹中新写一个记录cpu信息的文件
		:param package_name:测试包名
		:param url:cpu文件的路径
		:return:None
		"""
		self.cf.read('monkey.conf')
		self.cf.set('cpu_check', 'mark', 'True')
		self.cf.write(open('monkey.conf', 'w'))
		with open(self.get_dir(url), 'w') as f:
			while True:
				a = os.popen('adb shell dumpsys cpuinfo | grep ' + package_name)
				cpuinfo_list = a.readlines()[0].split(' ')
				if len(cpuinfo_list) == 13:
					cpu = [cpuinfo_list[2], cpuinfo_list[4], cpuinfo_list[7]]
					cpuinfo = ','.join(cpu)
					f.write(cpuinfo)
					f.write('\n')
					time.sleep(0.5)
					self.cf.read('monkey.conf')
					if self.cf.get('cpu_check', 'mark') == "False":
						break

	def get_meminfo(self, package_name):
		"""
		获取内存信息
		:return:str, 内存信息
		"""
		newlist = []
		f = os.popen('adb shell dumpsys meminfo ' + package_name)
		for x in f.readlines():
			newlist.append(x.strip())
		try:
			mem_total = newlist[8].split('   ')[7]
			mem_used = newlist[8].split('   ')[8]
			mem_free = newlist[8].split('   ')[9]
		except Exception:
			mem_total = ''
			mem_used = ''
			mem_free = ''
		meminfo = '{},{},{}'.format(mem_total, mem_used, mem_free)

		return meminfo

	def get_dir(self, url):
		"""
		获取最新的文本路径
		:return: str, 文本路径
		"""
		all_dir = os.listdir(os.getcwd() + "/device_info/" + url)
		nums = []
		for x in all_dir:
			if x.split('-')[0]:
				try:
					nums.append(int(x.split('-')[0]))
				except Exception:
					pass
		print "device_info/{}/{}-{}.txt".format(url, str(max(nums) + 1), self.get_devices())
		return "device_info/{}/{}-{}.txt".format(url, str(max(nums) + 1), self.get_devices())

	def get_pid(self, package_name):
		"""
		获取pid
		:param package_name:包名
		:return: str, pid
		"""
		pid = []
		f = os.popen('adb shell ps | grep ' + package_name)
		for x in f.readlines():
			pid_list = x.split(' ')
			for y in pid_list:
				if y.strip() == package_name:
					for z in x.split(' '):
						if z:
							pid.append(z)
		rst = pid[1]
		return rst

	def get_flow(self, package_name, mark):
		"""
		获取流量信息
		:param package_name:包名
		:param mark:获取流量的标记
		:return:
		"""
		if mark == "start":
			rst_list = []
			f = os.popen('adb shell cat /proc/{}/net/dev | grep wlan0'.format(self.get_pid(package_name)))
			for x in f.readlines():
				for y in x.split(' '):
					if y:
						rst_list.append(y)
			rst = int(rst_list[1]) + int(rst_list[9])
			conf_data = {
				'total': str(rst),
				'flowup': str(rst_list[9]),
				'flowdown': str(rst_list[1]),
				'timestart': str(time.time())
			}
			self.cf.read('monkey.conf')
			self.cf.set('flow_mark', 'flow_total', conf_data['total'])
			self.cf.set('flow_mark', 'flow_up', conf_data['flowup'])
			self.cf.set('flow_mark', 'flow_down', conf_data['flowdown'])
			self.cf.set('flow_mark', 'time_start', conf_data['timestart'])
			self.cf.write(open('monkey.conf', 'w'))
		else:
			rst_list = []
			f = os.popen('adb shell cat /proc/{}/net/dev | grep wlan0'.format(self.get_pid(package_name)))
			for x in f.readlines():
				for y in x.split(' '):
					if y:
						rst_list.append(y)
			rst = int(rst_list[1]) + int(rst_list[9])
			end_data = {
				'total': str(rst),
				'flowup': str(rst_list[9]),
				'flowdown': str(rst_list[1]),
				'timend': str(time.time())
			}
			self.cf.read('monkey.conf')
			oldTotal = self.cf.get('flow_mark', 'flow_total')
			oldUp = self.cf.get('flow_mark', 'flow_up')
			oldDown = self.cf.get('flow_mark', 'flow_down')
			oldTime = self.cf.get('flow_mark', 'time_start')
			rst_data = {
				'total': str(int(end_data['total']) - int(oldTotal)),
				'up': str(int(end_data['flowup']) - int(oldUp)),
				'down': str(int(end_data['flowdown']) - int(oldDown)),
				'time': str(float(end_data['timend']) - float(oldTime))
			}
			return rst_data

	def write_flow(self, package_name, url):
		self.cf.read('monkey.conf')
		self.cf.set('flow_mark', 'mark', 'True')
		self.cf.write(open('monkey.conf', 'w'))
		with open(self.get_dir(url), 'w') as fn:
			while True:
				rst_list = []
				f = os.popen('adb shell cat /proc/{}/net/dev | grep wlan0'.format(self.get_pid(package_name)))
				for x in f.readlines():
					for y in x.split(' '):
						if y:
							rst_list.append(y)
				up = rst_list[9]
				down = rst_list[1]
				flowInfo = '{},{}'.format(down, up)
				fn.write(flowInfo)
				fn.write('\n')
				print flowInfo
				time.sleep(0.5)
				self.cf.read('monkey.conf')
				if self.cf.get('flow_mark', 'mark') == "False":
					break

	def stop_flow(self):
		self.cf.read('monkey.conf')
		self.cf.set('flow_mark', 'mark', 'False')
		self.cf.write(open('monkey.conf', 'w'))

	def get_third_package(self):
		rst = []
		f = os.popen('adb shell pm list package -3')
		for x in f.readlines():
			rst.append(x.strip().split(':')[1])
		return rst

	def get_cur_pknm(self):
		try:
			f = os.popen('adb shell dumpsys window windows | grep mFocusedApp')
			for x in f.readlines():
				pknm = x.strip().split(' ')[4]
			pk_info = pknm.split('/')
			pk_data = {
				'errmsg': '查询成功',
				'package_name': pk_info[0],
				'avtivity_name': pk_info[1]
			}
		except Exception as e:
			pk_data = {
				'errmsg': '请确认设备正确连接或者是否有打开APP?'
			}
		return pk_data


if __name__ == '__main__':
	adb = Adb()
	# adb.stop_monkey()
	# print adb.get_devices()
	# adb.get_cpuinfo()
	# print adb.get_devices()

	# with open('device_info/meminfo/1.txt', 'w') as f:
	#     while check_mark:
	#         f.write(adb.get_meminfo('com.weizq'))
	#         f.write('\n')

	# adb.get_cpuinfo('com.weizq', 'cpuinfo')
	# adb.write_flow('com.weizq', 'flowinfo')
	# print adb.get_third_package()
	# print adb.get_cur_pknm()