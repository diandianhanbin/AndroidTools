from django.shortcuts import render
import os


# Create your views here.


def index(request):
	rightside = []
	result = []
	rst_data = []
	leftside = []
	passed = 0
	fail = 0
	noresult = 0
	with open(os.getcwd() + '/PortTest/leftside.txt') as ls:
		for x in ls.readlines():
			lf_data = {
				'code': x.strip().split('-')[0],
				'title': x.strip().split('-')[1]
			}
			leftside.append(lf_data)

	with open(os.getcwd() + '/PortTest/rightside.txt') as rs:
		for x in rs.readlines():
			row = x.strip().split('|')
			rs_data = {
				"fssj": row[0],
				"csbt": row[1],
				"fsfs": row[2],
				"alms": row[3],
				"fsdz": row[4],
				"fscs": row[5],
				'testid': row[6]
			}
			rightside.append(rs_data)

	with open(os.getcwd() + '/PortTest/result.txt') as rst:
		for x in rst.readlines():
			row = x.strip().split('|')
			if row[len(row)-1] == 'fail':
				fail += 1
			elif row[len(row)-1] == 'pass':
				passed += 1
			elif row[len(row)-1] == 'no except result':
				noresult += 1

			rs_data = []
			for y in row:
				rs_data.append(y)
			result.append(rs_data)
	for a, b in zip(rightside, result):
		data = {
			"sendData": a,
			"dealData": b,
			"result": b[len(b)-1]
		}
		rst_data.append(data)
	return render(request, 'PortTest/index.html', {"leftside": leftside,
													"rst_data": rst_data,
													"pass": passed,
													"fail": fail,
													"noresult": noresult})
