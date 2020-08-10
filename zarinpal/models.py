from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from food.models import FoodTransaction, SiteWallet
from .managers import PaymentTransactionManager


STATUS_CHOICES = (
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('F', 'Failed'),
)
class PaymentTransaction(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.DO_NOTHING,related_name='paytrans')
    amount = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES,default='P',max_length=10)
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    authority = models.CharField(blank=True, max_length=50)
    ref_id = models.CharField(blank=True, max_length=50)
    food_trans = models.OneToOneField(FoodTransaction,on_delete=models.DO_NOTHING,blank=True, null=True)
    wallet = models.ForeignKey(SiteWallet, on_delete=models.DO_NOTHING,blank=True, null=True)

    objects = PaymentTransactionManager()

    class Meta:
        verbose_name = ['لیست تراکنش']
        verbose_name_plural = ['لیست تراکنش ها']
        #ordering = ['-date_created']


    def __str__(self):
        return f"Owner: {self.owner}|Amount: {self.amount}|Status: {self.status}|RefID: {self.ref_id}"
    
    
    
