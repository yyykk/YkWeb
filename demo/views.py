from django.shortcuts import render
import pymysql
import json

# Create your views here.

from django.http import HttpResponse
 

def login(request):
	return render(request, 'login.html')
	
def GetSomething(request):
	return render(request, request.path[1:])
	
def Map(request):
	DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo")
	CursorDict = DataBase.cursor(pymysql.cursors.DictCursor)
	Cursor = DataBase.cursor()
	Cursor.execute('select ECI from tac;')
	ECI = Cursor.fetchall()
	position = []
	for e in ECI:
		CursorDict.execute(
	'''
		select t.lng, t.lat, e.Stream from ecihourstream as e, tac as t 
		where e.ECI = 
	'''
		+ str(e) + 'and e.ECI = t.ECI;')
		DictTemp = CursorDict.fetall()
		MaxStream = DictTemp['Stream'].max()
		for i in range(len(DictTemp['Stream'])):
			DictTemp['Stream'][i] = DictTemp['Stream'][i] / MaxStream
		position.append(DictTemp);
	#cursor.execute('select t.lng, t.lat, e.count from  tac as t, ecicounter as e where t.ECI = e.ECI')
	#position = cursor.fetchall()
	return render(request, 'map.html', {'position' : json.dumps(position)})#, {'lat' : lat})
	