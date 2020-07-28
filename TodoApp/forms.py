from django import forms
from .models import ToDoApp
from django.forms.widgets import SplitDateTimeWidget
from .widgets import BootstrapDateTimePickerInput


class ToDoAppForm(forms.ModelForm):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )
    class Meta:
        model = ToDoApp
        fields = '__all__'
        
        