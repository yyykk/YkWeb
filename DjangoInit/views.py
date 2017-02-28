#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
 
def index(request):
    return HttpResponse(u"欢迎光临 玉师傅之家!")

def add(request):
	a = request.GET['a']
	b = request.GET['b']
	c = int(a) + int(b)
	return HttpResponse(str(c))

def add2(request, a, b):
	c = int(a) + int(b)
	return HttpResponse(str(c))
	
def index(request):
	return render(request, 'home.html')