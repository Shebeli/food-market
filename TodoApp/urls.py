from django.urls import path
from .views import todoview

urlpatterns = [
    path('', todoview , name='todo-list'),
]