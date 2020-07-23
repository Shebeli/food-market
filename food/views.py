from django.shortcuts import render, redirect, reverse
from django.http import Http404
from django.views.generic import ListView, FormView, DetailView, UpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.views import View
from django.contrib import messages
from django.core.validators import validate_integer
from .models import TheFood, SiteWallet
from .forms import SiteUserCreationForm, DepositForm, WithdrawForm

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

class WalletDetailView(DetailView):
    model = SiteWallet
    #queryset = SiteWallet.objects.filter(owner=request.use)
    context_object_name = 'sitewallet'
        
    def get(self, request, *args, **kwargs):
        self.object = SiteWallet.objects.get(owner=request.user)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class WalletDepositView(FormView):
    model = SiteWallet
    form_class = DepositForm
    success_url = '../'
    #queryset = SiteWallet.objects.filter(owner=request.user)

    def get_object(self):
        if self.request.user.is_authenticated:
            self.object = SiteWallet.objects.get(owner=self.request.user)
            return self.object
        else:
            return Http404("Wallet not found")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            amount = int(request.POST.get('deposit'))
            self.object = self.get_object()
            self.object.deposit(amount)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class WalletWithdrawView(FormView):
    model = SiteWallet
    form_class = WithdrawForm
    success_url = '../'
    #queryset = SiteWallet.objects.filter(owner=request.user)

    def get_object(self):
        if self.request.user.is_authenticated:
            self.object = SiteWallet.objects.get(owner=self.request.user)
            return self.object
        else:
            return Http404("Wallet not found")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            amount = int(request.POST.get('withdraw'))
            self.object = self.get_object()
            if self.object.balance <= amount:
                messages.error(request,"مقدار ذکر شده بیشتر از موجودی است")
                return redirect('wallet-withdraw')
            self.object.withdraw(amount)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
            


    
    

