# ecoding=utf-8
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
import adb
ad = adb.Adb()

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def index(request):
	return render(request, 'index.html')


@csrf_exempt
def setuptools(request):
	url = os.getcwd()
	os.system('python {}/run.py'.format(url))
	return HttpResponse('True')


@csrf_exempt
def getMemData(request, filename):
	user_rst = []
	total_rst = []
	url = '{}/device_info/meminfo/{}.txt'.format(os.getcwd(), filename)
	with open(url, 'r') as f:
		for x in f.readlines():
			user_rst.append(x.strip().split(',')[2].strip())
			total_rst.append(x.strip().split(',')[0].strip())
	rst_data = {
		'status': 200,
		'title': '内存监控信息',
		'desc': '内存信息',
		'name': '内存监控',
		'user_data': user_rst,
		'total_data': total_rst,
	}
	return JsonResponse(rst_data)


@csrf_exempt
def getDirList(request, cate):
	rst = []
	url = '{}/device_info/{}'.format(os.getcwd(), cate)
	old_rst = os.listdir(url)
	old_rst.pop(0)
	for x in old_rst:
		rst.append(x.split('.')[0])
	rst_data = {
		'status': 200,
		'data': rst[::-1]
	}
	return JsonResponse(rst_data)


def mem_info(request):
	return render(request, 'mem_info.html')


def cpu_info(request):
	return render(request, 'cpu_info.html')


@csrf_exempt
def getCpuData(request, filename):
	total_cpu = []
	user_cpu = []
	url = '{}/device_info/cpuinfo/{}.txt'.format(os.getcwd(), filename)
	with open(url, 'r') as f:
		for x in f.readlines():
			total_cpu.append(x.strip().split(',')[0].strip()[:-1])
			user_cpu.append(x.strip().split(',')[2].strip()[:-1])
		rst_data = {
			'status': 200,
			'total_data': total_cpu,
			'user_data': user_cpu
		}
	return JsonResponse(rst_data)


def flowinfo(request):
	return render(request, 'flow.html')


def getFlowInfo(request, filename):
	url = '{}/device_info/flowinfo/{}.txt'.format(os.getcwd(), filename)
	up = []
	down = []
	with open(url, 'r') as f:
		for x in f.readlines():
			up_data = str(round(float(x.split(',')[1])/1024/1024, 2))
			down_data = str(round(float(x.split(',')[0])/1024/1024, 2))
			up.append(up_data)
			down.append(down_data)
		rst_data = {
			'status': 200,
			'up': up,
			'down': down
		}
	return JsonResponse(rst_data)


def flowTest(request):
	if request.GET.get('mark') == 'start':
		mark = request.GET.get('mark')
		package_name = request.GET.get('package')
		ad.get_flow(package_name, mark)
		ad.write_flow(package_name, 'flowinfo')
	else:
		ad.stop_flow()
		package_name = request.GET.get('package')
		mark = request.GET.get('mark')
		rst = ad.get_flow(package_name, mark)
		return JsonResponse(rst)
	return HttpResponse('hello')


def get_cur_pknm(request):
	data = ad.get_cur_pknm()
	return JsonResponse(data)


def get_third_pknm(request):
	data = {
		'third_pknm': ad.get_third_package(),
		'errmsg': 'ok'
	}
	return JsonResponse(data)