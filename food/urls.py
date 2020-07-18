from django.urls import path
from .views import TheFoodListView, UserRegisterFormView

urlpatterns = [
    path('', TheFoodListView.as_view(template_name="food/foods.html"), name="food-list"),
    path('register/', UserRegisterFormView.as_view(template_name="food/register.html"), name='register'),
]