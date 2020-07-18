from django.shortcuts import render
from django.views.generic import ListView, FormView
from .models import TheFood
from .forms import SiteUserCreationForm

class TheFoodListView(ListView):
    model = TheFood
    paginate_by = 20
    context_object_name = "food_list"

class UserRegisterFormView(FormView):
    form_class = SiteUserCreationForm
    success_url = '../'

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
