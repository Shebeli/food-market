from django.urls import path
from .views import todoview, tododelete

urlpatterns = [
    path('', todoview , name='todo-list'),
    path('delete/<int:id>/', tododelete , name='todo-delete'),
]