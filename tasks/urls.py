from django.urls import path

from . import views, views_categories

app_name="tasks"

urlpatterns = [
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),

    path("tasks/", views.index, name="index",),
    path("tasks/create/", views.create, name="create"),
    path("tasks/edit/<int:id>/", views.update, name="update"),
    path("tasks/delete/<int:id>/", views.delete, name="delete"),

    path("categories/", views_categories.index, name="categories"),
    path("categories/edit/<int:id>/", views_categories.update, name="update_category"),
    path("categories/delete/<int:id>/", views_categories.delete, name="delete_category"),
]