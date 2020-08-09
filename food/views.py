from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, FormView, DetailView, UpdateView
from django.views.generic.base import TemplateResponseMixin, TemplateView, RedirectView
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.views import View
from django.contrib import messages
from django.core.validators import validate_integer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TheFood, SiteWallet, FoodTransaction, FoodCount
from .forms import SiteUserCreationForm, DepositForm, WithdrawForm
from zarinpal.models import PaymentTransaction

def get_trans(user):
        """Retrieves the latest food transaction.
        If theres no transaction availabe, then create one."""
        transactions = FoodTransaction.objects.filter(owner=user)
        for trans in transactions:
            if trans.completed == False:
                return trans
            elif trans.completed == True:
                continue
        trans = FoodTransaction.objects.create(owner=user)
        return trans
        
def get_payment(wallet):
        """Get the associated payment object or create it.(For deposit incases only)"""
        #pay, created= PaymentTransaction.objects.get_or_create(wallet=wallet, owner=wallet.owner)
        try:                              
            pay = PaymentTransaction.objects.get(wallet=wallet, owner=wallet.owner)
        except ObjectDoesNotExist:
            pay = PaymentTransaction.objects.create(wallet=wallet, owner=wallet.owner)
        return pay

class TheFoodListView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['food_list'] = TheFood.objects.all()
            trans = get_trans(self.request.user)
            context['food_count'] = FoodCount.objects.filter(transaction=trans)
            context['transaction'] = trans
            return context
        return context        

class FoodListRedirectView(RedirectView):

    permanet = False
    pattern_name = 'food-list'

    def get_redirect_url(self, *args, **kwargs):
        trans = get_trans(self.request.user)
        status = trans.complete_trans_with_wallet(self.request.user)
        if status:
            messages.success(self.request,"Transaction completed successfully.")
            return super().get_redirect_url(*args, **kwargs)
        messages.error(self.request,"You do not have enough currency.")
        return super().get_redirect_url(*args, **kwargs)



def additemview(request, id):
    trans = get_trans(request.user)
    food = TheFood.objects.get(pk=id)
    trans.add_food(food)
    return redirect('food-list')

def removeitemview(request, id):
    trans = get_trans(request.user)
    food = TheFood.objects.get(pk=id)
    trans.remove_food(food)
    return redirect('food-list')

def countincview(request, id):
    trans = get_trans(request.user)
    food = TheFood.objects.get(pk=id)
    trans.increment_food(food)
    return redirect('food-list')

def countdecview(request, id):
    trans = get_trans(request.user)
    food = TheFood.objects.get(pk=id)
    trans.decrement_food(food)
    return redirect('food-list')


class UserRegisterFormView(FormView):
    form_class = SiteUserCreationForm
    success_url = '../'

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class WalletDetailView(LoginRequiredMixin ,DetailView):
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

    def post(self, request, *args, **kwargs):# for zarinpal
        form = self.get_form()
        if form.is_valid():
            amount = int(request.POST.get('deposit'))
            self.object = self.get_object()
            pay = get_payment(self.object)
            pay.amount = amount 
            pay.save()
            request.session['ok'] = True 
            return redirect(reverse('zarinpal:send-request', kwargs={'pk': pay.pk}))
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())

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

    
        
            


    
    

