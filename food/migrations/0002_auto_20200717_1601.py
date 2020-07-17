# Generated by Django 3.0.8 on 2020-07-17 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='phone_number',
            field=models.IntegerField(error_messages={'unique': 'این شماره قبلا ثبت شده است'}, null=True, unique=True, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='نام خانوادگی'),
        ),
    ]
