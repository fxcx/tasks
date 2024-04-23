from django.shortcuts import render, redirect
from .forms import TaskForm, CategoryForm
from .models import Task, Category


def index(request):
    if request.user.is_authenticated is False:
        return redirect("tasks:login")
    
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.user = request.user
            instance.save()
             
    default_category = Category.objects.get(pk=1)
    categories = [default_category]
    user_categories = Category.objects.filter(user=request.user)
    if user_categories:
        categories.extend(user_categories)

    form = CategoryForm()
    
    return render(
        request,
        "categories.html",
        {"categories": categories, "form":form},
    )


def update(request, id):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category.objects.get(pk=id)
            category.name = form.cleaned_data['name']
            category.save()
            return redirect("tasks:index")

    else:
        task = Category.objects.get(pk=id)
        form = CategoryForm(instance= task)

    return render(request, "create.html", {"form": form , "id":id})

def delete(request, id):
    task = Task.objects.get(pk=id)
    task.delete()
    return redirect("tasks:index") 
