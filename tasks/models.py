from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

# class User(models.Model):
#     email = models.EmailField(null=False, max_length=100, unique=True, blank=False)
#     password = models.CharField(max_length=128)

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     def __str__(self) -> str:
#         return self.email



class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @classmethod
    def get_default_category(cls):
        default_category, _ = cls.objects.get_or_create(name="No category", user=None)
        return default_category

    def __str__(self) -> str:
        return self.name



class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=Category.get_default_category
    )


    def __str__(self) -> str:
        return self.title + ", " + self.user.email  