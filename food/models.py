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
        return f"{self.name}: {self.price}$"
 
 
class FoodTransaction(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    total_price = models.IntegerField(default=0,verbose_name='مجموع هزینه')
    date_modified = models.DateTimeField(auto_now=True,verbose_name='تاریخ صورت حساب')
    completed = models.BooleanField(default=False,verbose_name='انجام شده')
    foods = models.ManyToManyField(TheFood,through='FoodCount',blank=True)

    def __str__(self):
        return f"Owner: {self.owner} | Total price: {self.total_price}$ | Completed: {self.completed} | DateModified: {self.date_modified}| ID: {self.pk} |"

    def add_food(self, food):# food is the selected thefood object. eg: food = TheFood.objects.get(pk=pk)
        """Adds the given object food to the transaction querylist and increase foodtrans total_price based on food's price."""
        self.foods.add(food)
        count_obj = self.foodcount_set.get(food=food, transaction=self)
        count_obj.count += 1
        self.total_price += food.price
        self.save()
        count_obj.save()

    def increment_food(self, food):# food is the selected thefood object. eg: food = TheFood.objects.get(pk=pk)
        """Increments food count by 1 for the count object"""
        count_obj = self.foodcount_set.get(food=food, transaction=self)
        count_obj.count += 1
        self.total_price += food.price
        self.save()
        count_obj.save()

    def remove_food(self, food):
        """Removes the given object food from the transaction and decrease foodtrans total_price based on food's price."""
        count_obj = self.foodcount_set.get(food=food, transaction=self)
        self.total_price -= count_obj.count * food.price 
        self.foods.remove(food)#FoodCount associated object will also be deleted
        self.save()

    def decrement_food(self, food):# food is the selected thefood object. eg: food = TheFood.objects.get(pk=pk)
        """Decrements food count by 1 for the given foodtransaction object. if the count is less than one, remove it instead."""
        count_obj = self.foodcount_set.get(food=food, transaction=self)
        if count_obj.count <= 1:
            self.remove_food(food)
        else:
            count_obj.count -= 1
            self.total_price -= food.price
            self.save()
            count_obj.save()

    def complete_trans_with_wallet(self, user):
        """Complete the transaction with wallet currency; If the wallet doesn't have enough currency,
        return false"""#also, maybe the information about the foodtransaction must be parsed into json or sth for API usage...
        wallet = SiteWallet.objects.get(owner=user)    
        cost = self.total_price
        if wallet.balance >= cost:
            wallet.withdraw(cost)
            self.completed = True
            self.save()
            return True
        else:
            return False


class FoodCount(models.Model):
    food = models.ForeignKey(TheFood, on_delete=models.PROTECT)
    transaction = models.ForeignKey(FoodTransaction, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Food: {self.food},count: {self.count}, Transaction: {self.transaction.id , self.transaction.owner}, "

class SiteWallet(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
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

    
