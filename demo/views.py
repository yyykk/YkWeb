from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
 

def login(request):
	return render(request, 'login.html')
	
def GetSomething(request):
	return render(request, request.path[1:])