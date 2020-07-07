from django.shortcuts import render, redirect
from .forms import ToDoAppForm
from .models import ToDoApp
from django.views.generic import ListView, CreateView, DeleteView

#class ToDoView(ListView):
    #model = ToDoApp
    #queryset = ToDoApp.objects.all()
    #template_name = 'TodoApp/todo.html'

def todoview(request):
    if request.method == 'POST':
        form = ToDoAppForm(request.POST)
        if form.is_valid():
            form.save()
            form = ToDoAppForm()
    else:
        form = ToDoAppForm()

    qs = ToDoApp.objects.all()
    context = {'form': form, 'object_list': qs}
    return render(request, 'TodoApp/todo.html', context)

def tododelete(request, id):
    obj = ToDoApp.objects.get(id=id)
    obj.delete()

    return redirect('todo-list')
