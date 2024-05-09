from django.forms import ModelForm
from .models import Task, Category

class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            #! no funciona
            # default_category = Category.objects.filter(pk=1)
            # user_categories = Category.objects.filter(user=user)
            # categories = default_category.union(user_categories)
            # self.fields['category'].queryset = categories

            categories = Category.objects.filter(pk=1) | Category.objects.filter(user=user)
            self.fields['category'].queryset = categories.distinct()
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed','category']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']