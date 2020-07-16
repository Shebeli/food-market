from django.urls import path
from .views import TheFoodListView

urlpatterns = [
    path('', TheFoodListView.as_view(template_name="food/foods.html"), name="food-list"),
]