from django.contrib import admin
from .models import TheFood, SiteUser, SiteWallet, WalletTransactions
from django.contrib.auth.admin import UserAdmin

admin.site.register(TheFood)
admin.site.register(SiteWallet)
admin.site.register(WalletTransactions)
admin.site.register(SiteUser, UserAdmin)
