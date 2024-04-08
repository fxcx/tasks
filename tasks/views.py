from django.http import HttpResponse
from django.contrib.auth import  login, logout

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


def register(request):
    if request.user.is_authenticated:
       return redirect("tasks:index")
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            # username = form.cleaned_data["username"]
            # password = form.cleaned_data["password1"]

            # user = User.objects.create_user(username=username, password=password)
            login(request, user)

            if request.user.is_authenticated:
                return redirect("tasks:index")
            
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def index(request):
    if request.user.is_authenticated is False :
        return redirect("tasks:login")
    
    return render(request,"index.html", {"user":request.user})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("tasks:index")
     
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("tasks:index")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    print(request.user.is_authenticated )
    if request.user.is_authenticated:
        print('sigue logueado')

    return redirect("tasks:index")
