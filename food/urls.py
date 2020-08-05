from django.urls import path
from .views import (TheFoodListView, UserRegisterFormView, WalletDetailView, FoodListRedirectView,
                    WalletDepositView, WalletWithdrawView, additemview, removeitemview, countincview, countdecview )

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', TheFoodListView.as_view(template_name="food/foods.html"), name="food-list"),
    path('login/', LoginView.as_view(template_name="food/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="food/logout.html"), name='logout'),
    path('register/', UserRegisterFormView.as_view(template_name="food/register.html"), name='register'),
    path('wallet/', WalletDetailView.as_view(template_name="food/wallet.html"), name="wallet"),
    path('wallet/deposit/',WalletDepositView.as_view(template_name="food/wallet_deposit.html"), name="wallet-deposit"),
    path('wallet/withdraw/',WalletWithdrawView.as_view(template_name="food/wallet_withdraw.html"), name="wallet-withdraw"),
    path('add_food/<int:id>/', additemview, name='add-item'),
    path('remove_food/<int:id>/', removeitemview, name='remove-item'),
    path('inc_food/<int:id>/', countincview, name='increase-item'),
    path('dec_food/<int:id>/', countdecview, name='decrease-item'),
    path('wallet/transaction/', FoodListRedirectView.as_view(), name='foodwallet-transaction')
]