from django import forms
from .models import ToDoApp
from django.forms.widgets import SplitDateTimeWidget
from .widgets import BootstrapDateTimePickerInput


class ToDoAppForm(forms.ModelForm):
    date = forms.TimeField(
        input_formats=['%H:%M'],
        help_text='eg. 15:30'
    )
    class Meta:
        model = ToDoApp
        fields = '__all__'
        
        