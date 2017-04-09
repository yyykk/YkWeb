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
    DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo", charset='utf8')
    CursorDict = DataBase.cursor(pymysql.cursors.DictCursor)
    Cursor = DataBase.cursor()
    Cursor.execute('select distinct Time from EciTimeStream;')
    Time = Cursor.fetchall()
    position = []
    for t in Time:
        #print("select t.lng, t.lat, e.Stream / m.MStream * 100 as count from ecihourstream as e , MaxStream as m, tac as t where t.ECI = e.ECI and e.ECI = m.ECI and e.Time = '" + str(t)[2:15] + "'")
        CursorDict.execute("select t.lng, t.lat, e.Stream as count from EciTimeStream as e, tac as t where t.ECI = e.ECI and e.Time = '" + str(t)[2:6] + "'")
        DictTemp = CursorDict.fetchall()
        #print(DictTemp)
        position.append(DictTemp)
    #print(position[6])
    DataBase.close()
    return render(request, 'map.html', {'position' : json.dumps(position)})
	
def MotorwayTAC(request):
    DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo", charset='utf8')
    Cursor = DataBase.cursor()
    Cursor.execute('select distinct lng, lat from motoway;')
    position = Cursor.fetchall();
    #print(position[6])
    DataBase.close()
    return render(request, 'MotorwayTAC.html', {'position' : json.dumps(position)})
	
def MotorwayStream(request):
	DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo", charset='utf8')
	CursorDict = DataBase.cursor(pymysql.cursors.DictCursor)
	position = [];
	CursorDict.execute("select s.Stream / 6004098604 as count, m.lng, m.lat from MotorEciStream as s, motoway as m where s.ECI = m.ECI;")
	DictTemp = CursorDict.fetchall()
	position.append(DictTemp);
	CursorDict.execute("select (s.amount / 5658) as count, m.lng, m.lat from MotorWayPeople as s, motoway as m where s.ECI = m.ECI;")
	DictTemp = CursorDict.fetchall()
	position.append(DictTemp);
	DataBase.close()
	return render(request, 'MotorwayStream.html', {'position' : json.dumps(position)})
	
	
	
	
	
	
	
	
	