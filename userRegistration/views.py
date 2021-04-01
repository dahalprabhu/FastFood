from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
    # Create your views here.

def index(request):
    return render(request, 'home.html', {'name':'anup'})

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST' :
        username=request.POST['username']
        password= request.POST['password']
        user= User.objects.create_user(username= username, password=password)
        user.save()
        print('user created')
        return redirect('/account/login/')
    else:
        return render(request , 'register.html')


