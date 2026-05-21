from django.urls import path

from . import views

app_name = "cocktails"

urlpatterns = [
    path("", views.index, name="recipe_list"),
    path("create/", views.recipe_create, name="recipe_create"),
    path("<int:pk>/edit/", views.recipe_edit, name="recipe_edit"),
    path("<int:pk>/delete/", views.recipe_delete, name="recipe_delete"),
    path("<int:pk>/", views.recipe_detail, name="recipe_detail"),
]
