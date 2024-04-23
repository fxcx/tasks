from django.contrib.auth import login, logout

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import TaskForm
from .models import Task, Category


def register(request):
    if request.user.is_authenticated:
        return redirect("tasks:index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data["username"]
            # password = form.cleaned_data["password1"]

            # user = User.objects.create_user(username=username, password=password)
            login(request, user)

            if request.user.is_authenticated:
                return redirect("tasks:index")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


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
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        print("sigue logueado")

    return redirect("tasks:index")


def index(request):

    if request.user.is_authenticated is False:
        return redirect("tasks:login")

    if request.GET.get('state') is None:
        state = "all"
    else:
        state = request.GET["state"]
    
    if request.GET.get('category') is None:
        category = "all"
    else:
        category = request.GET["category"]
    
    if state == "all" and category == "all":
        tasks = Task.objects.filter(user=request.user)
    elif state == "all" and category != "all":
        selected_category = Category.objects.get(name=category)
        tasks = Task.objects.filter(user__id=request.user.id , category__id= selected_category.id )
    elif state != "all" and category == "all":
        selected_state = state == 'completed'
        tasks = Task.objects.filter(user__id=request.user.id, completed= selected_state)
    else:
        # state != "all" and category != "all":
        selected_state = state == 'completed'
        selected_category = Category.objects.get(name=category)
        tasks = Task.objects.filter(user__id=request.user.id , category__id= selected_category.id, completed= selected_state )


    default_category = Category.objects.get(pk=1)
    categories = [default_category]
    user_categories = Category.objects.filter(user=request.user)
    if user_categories:
        categories.append(user_categories)

    return render(
        request,
        "index.html",
        {"user": request.user, "tasks": tasks, "categories": categories, "state":state, "category":category},
    )


def create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("tasks:index")

    else:
        form = TaskForm()

    return render(request, "create.html", {"form": form})

def update(request, id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task.objects.get(pk=id)
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.completed = form.cleaned_data['completed']
            task.category = form.cleaned_data['category']

            task.save()
            return redirect("tasks:index")

    else:
        task = Task.objects.get(pk=id)
        form = TaskForm(instance= task)

    return render(request, "create.html", {"form": form , "id":id})

def delete(request, id):
    task = Task.objects.get(pk=id)
    task.delete()
    return redirect("tasks:index") 
