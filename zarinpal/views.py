from django.http import HttpResponse
from django.shortcuts import redirect , render
from zeep import Client
from django.conf import settings

# Zarinpal's sandbox webservice: "https://sandbox.zarinpal.com/pg/services/WebGate/wsdl"
# Zarinpal's sandbox payservice: "https://sandbox.zarinpal.com/pg/StartPay/"
sandbox = getattr(settings, ZARINPAL_SANDBOX, False)
merchant = getattr(settings, MERCHANT_ID, None)
callback_url = getattr(settings, ZARINPAL_REDIRECT_URL, None)

if not redirect_url:
    raise Exception("Specify ZARINPAL_REDIRECT_URL")

if sandbox:
    client = Client("https://sandbox.zarinpal.com/pg/services/WebGate/wsdl")
    payment = "https://sandbox.zarinpal.com/pg/StartPay/"
    merchant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
elif not sandbox:
    client = Client("https://zarinpal.com/pg/services/WebGate/wsdl")
    payment = "https://zarinpal.com/pg/StartPay/"
else:
    raise Exception("Please specify the boolean value of ZARINPAL_SANDBOX in settings")

if not sandbox and not merchant:
    raise Exception("Set the id of MERCHANT_ID in settings.")

#MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
#client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'test12345@gmail.com'  # Optional
mobile = '09123456789'  # Optional
#CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.

def send_request(request):
    result = client.service.PaymentRequest(merchant, amount, description, email, mobile, callback_url)
    if result.Status == 100:
        return redirect(payment + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(merchant, request.GET['Authority'], amount)
        if result.Status == 100:
            context = {'REF_ID': str(result.RefID)}
            #render(request,'zarinpal/success.html')
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            context = {'status': str(result.Status)}
            #render(request,'zarinpal/pending.html')
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            context = {'status': str(result.Status)}
            #render(request,'zarinpal/failed.html')
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')