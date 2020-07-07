from django import forms
from .models import ToDoApp
from django.forms.widgets import SplitDateTimeWidget


class ToDoAppForm(forms.ModelForm):
    #date = forms.SplitDateTimeField(widget=SplitDateTimeWidget)
    class Meta:
        model = ToDoApp
        fields = '__all__'
        
        