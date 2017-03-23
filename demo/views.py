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
	