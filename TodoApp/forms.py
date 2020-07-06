from django import forms
from .models import ToDoApp


class ToDoAppForm(forms.ModelForm):
    class Meta:
        model = ToDoApp
        fields = '__all__'