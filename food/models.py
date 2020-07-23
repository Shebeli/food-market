from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    first_name = models.CharField(max_length=30,blank=True,verbose_name='نام')
    last_name = models.CharField(max_length=30,blank=True,verbose_name='نام خانوادگی')
    phone_number = models.IntegerField(verbose_name='شماره تلفن',unique=True,
    error_messages={'unique':'این شماره قبلا ثبت شده است'},
    blank=False,null=True,help_text='شماره در 10 رقم به صورت  ******9'
    )
    email = models.EmailField(verbose_name='ایمیل',blank=False)

class TheFood(models.Model):
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    price = models.IntegerField()
    image = models.ImageField(width_field=250, height_field=250, blank=True, null=True)

    def __str__(self):
        return f"{self.name} --> {self.price}"

class SiteWallet(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField(verbose_name='مقدار حساب',default=0)

    def get_absolute_url(self):
        return reverse("wallet") #args=[str(self.id)] the keyword argument would return 
                                                                #sth like: pk=3; while the arg returns: 3 
    
    def __str__(self):
        return f"{self.owner}: {self.balance}$"

    def deposit(self, amount):
        self.balance += amount
        WalletTransactions.objects.create(amount=amount, new_balance=self.balance,kind='DP')
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            WalletTransactions.objects.create(amount=amount, new_balance=self.balance,kind='WD')
            self.save()
        else:
            return None

class WalletTransactions(models.Model):
    amount = models.IntegerField()
    new_balance = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    kind = models.TextField(choices=[('DP','واریز'),('WD','برداشت')])

    def __str__(self):
        return f"type: {self.kind} | amount: {self.amount} --> New balance: {self.new_balance}"

    
