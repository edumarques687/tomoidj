from django.shortcuts import render, redirect
from jutsu.models import Jutsu
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def about(request):
    jutsus = Jutsu.objects.all().order_by('name')
    return render(request, 'homepage/home.html', {'jutsus': jutsus})

@csrf_protect
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'homepage/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/tome/g/')
            except IntegrityError:
                return render(request, 'homepage/signupuser.html', {'form': UserCreationForm(), 'error':'Este usuário não está disponível'})
        else:
            return render(request, 'homepage/signupuser.html', {'form': UserCreationForm(), 'error':'As senhas devem ser iguais.'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'homepage/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'homepage/loginuser.html', {'form': AuthenticationForm(), 'error': 'Usuário e/ou senha incorreta!'})
        else:
            login(request, user)
            return redirect('/tome/g/')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'homepage/home.html')

def help(request):
    return render(request, 'homepage/help.html')
