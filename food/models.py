from django.db import models
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


