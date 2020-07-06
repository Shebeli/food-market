from django.shortcuts import render
from .forms import ToDoAppForm
from .models import ToDoApp
from django.views.generic import ListView, CreateView, DeleteView

class ToDoListView(ListView):
    model = ToDoApp
    queryset = ToDoApp.objects.all()
    template_name = 'TodoApp/todo.html'
    
class ToDoCreateView(CreateView):
    pass 

class ToDoDeleteView(DeleteView):
    pass