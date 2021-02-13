from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Entry
from .models import Setting
from django.contrib.auth import authenticate, logout, login
# Create your views here.


def index(request):
	entries=Entry.objects.all().order_by('-id')
	context = {
		'entries' : entries,
	}
	return render(request, 'dashboard/index.html',context)
def entrydetail(request,id):
	entry=Entry.objects.get(pk=id)
	context = {
		'entry' : entry,
	}
	return render(request, 'dashboard/showentrydetail.html',context)
def register(request):
    return render(request, 'dashboard/register.html')
def setting(request):
	minimum=Setting.objects.get(name="minimum")
	expiry=Setting.objects.get(name="expiry")
	context = {
		'minimum' : minimum,
		'expiry' : expiry,
	}
	return render(request, 'dashboard/setting.html',context)
def saveexpiry(request):
	Setting.objects.filter(name="expiry").update(value=request.POST['minimumexpiry'])
	return redirect('dashboard:setting')
def saveminimum(request):
	Setting.objects.filter(name="minimum").update(value=request.POST['minimumstock'])
	return redirect('dashboard:setting')

def userlogin(request):
	if request.method == 'POST':    
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			return render(request, 'dashboard/login.html')
	else:
		return render(request, 'dashboard/login.html')
def userlogout(request):
	logout(request)
	return redirect('/')