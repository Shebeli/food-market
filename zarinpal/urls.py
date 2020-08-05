from django.urls import path
from .views import verify_payment, send_request, SessionView, foodpayment
from django.views.generic import TemplateView

app_name = 'zarinpal'
urlpatterns = [
    path('request/<int:pk>/', send_request, name='send-request'),
    path('verify/<int:pk>/', verify_payment, name='verify'),
    path('transaction/', foodpayment, name='startpay'),
    path('success/', SessionView.as_view(template_name='zarinpal/success.html'), name='success'),
    path('pending/', SessionView.as_view(template_name='zarinpal/pending.html'), name='pending'),
    path('failed/', SessionView.as_view(template_name='zarinpal/failed.html'), name='failed'),
    
]