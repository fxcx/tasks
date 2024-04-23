from django.shortcuts import render, redirect
from .forms import TaskForm, CategoryForm
from .models import Task, Category


def index(request):
    if request.user.is_authenticated is False:
        return redirect("tasks:login")

    default_category = Category.objects.get(pk=1)
    categories = [default_category]
    user_categories = Category.objects.filter(user=request.user)
    if user_categories:
        categories.append(user_categories)

    form = CategoryForm()

    return render(
        request,
        "categories.html",
        {"categories": categories, "form":form},
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
