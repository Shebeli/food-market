from django.http import HttpResponse
from django.shortcuts import redirect , render, reverse
from zeep import Client
from django.conf import settings
from django.views.generic import TemplateView
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import PaymentTransaction
from food.views import get_trans
from django.core.exceptions import ObjectDoesNotExist
from . import exceptions

# Zarinpal's sandbox webservice: "https://sandbox.zarinpal.com/pg/services/WebGate/wsdl"
# Zarinpal's sandbox payservice: "https://sandbox.zarinpal.com/pg/StartPay/"

sandbox = getattr(settings, "ZARINPAL_SANDBOX", False)
merchant = getattr(settings, "MERCHANT_ID", None)
#callback_url = getattr(settings, "ZARINPAL_REDIRECT_URL", None)
#callback_url = reverse('verify',kwargs={'pk':})

#if not callback_url:
    #raise exceptions.CallbackurlException

if sandbox:
    client = Client("https://sandbox.zarinpal.com/pg/services/WebGate/wsdl")
    payment = "https://sandbox.zarinpal.com/pg/StartPay/"
    merchant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
elif not sandbox:
    client = Client("https://zarinpal.com/pg/services/WebGate/wsdl")
    payment = "https://zarinpal.com/pg/StartPay/"
else:
    raise exceptions.ZarinPalSandBoxException

if not sandbox and not merchant:
    raise exceptions.MerchantIDException

email = 'test12345@gmail.com'  # Optional
mobile = '09123456789'  # Optional


def get_payment(foodtrans):
        """get the associated payment object or create it.(update it incase it got changed)"""
        try:                               # filters the P and F types
            pay = PaymentTransaction.objects.notcomplete().get(food_trans=foodtrans)
            pay.amount = foodtrans.total_price
            pay.save()
        except ObjectDoesNotExist:
            pay = PaymentTransaction.objects.create(owner=foodtrans.owner, amount=foodtrans.total_price, food_trans=foodtrans)
        return pay

#This validation and sorta of stuff can be refactored into better code
def send_request(request, pk):
    if not request.session['ok']:
        raise Http404
    payobj = PaymentTransaction.objects.get(pk=pk)
    amount = payobj.amount
    if amount <= 1000:
        raise exceptions.TooSmallException("At least 1000 is required to proceed")
    if not payobj.owner == request.user:
        raise Http404
    del request.session['ok']
    description = f" جمع تراکنش {payobj.amount}"
    callback_url = "http://127.0.0.1:8000" + reverse('zarinpal:verify',kwargs={'pk': pk})
    result = client.service.PaymentRequest(merchant, amount, description, email, mobile, callback_url)
    if result.Status == 100:
        payobj.authority = str(result.Authority)
        payobj.save()
        request.session['amount'] = amount
        return redirect(payment + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify_payment(request, pk):
    if request.GET.get('Status') == 'OK':
        payobj = PaymentTransaction.objects.get(pk=pk)
        amount = payobj.amount
        result = client.service.PaymentVerification(merchant, request.GET['Authority'], amount)
        payobj.authority = request.GET['Authority']
        payobj.save()
        if result.Status == 100:
            request.session['ref_id'] = str(result.RefID)
            request.session['valid'] = True
            payobj.status = 'C'
            if payobj.food_trans:
                payobj.food_trans.completed = True
                payobj.food_trans.save()
            else:
                payobj.wallet.balance += amount
                payobj.wallet.save()
            payobj.ref_id = str(result.RefID)
            payobj.save()
            context = {'REF_ID': str(result.RefID)}
            return redirect(reverse('zarinpal:success'))
        elif result.Status == 101:
            request.session['status'] = str(result.Status)
            request.session['valid'] = True
            payobj.status = 'P'
            payobj.save()
            return redirect(reverse('zarinpal:pending'))
        else:
            request.session['status'] = str(result.Status) # in template, use {{ request.session.status }}
            request.session['valid'] = True
            payobj.status = 'F'
            payobj.save()
            return redirect(reverse('zarinpal:failed'))
    else:
        payobj = PaymentTransaction.objects.get(pk=pk)
        payobj.status = 'F'
        payobj.save()
        return redirect(reverse('zarinpal:failed'))

class SessionView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.session['valid']:
                del self.request.session['valid']
                return super().render_to_response(context, **response_kwargs)
            raise Http404
        except KeyError:
            raise Http404

@login_required
def foodpayment(request):
    trans = get_trans(request.user)
    pay = get_payment(trans)
    request.session['ok'] = True
    return redirect(reverse('zarinpal:send-request', kwargs={'pk': pay.pk}))

    


    


