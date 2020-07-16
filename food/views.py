from django.shortcuts import render
from django.views.generic.list import ListView
from .models import TheFood

class TheFoodListView(ListView):
    model = TheFood
    paginate_by = 20
    context_object_name = "food_list"
    
