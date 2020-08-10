# Generated by Django 3.0.8 on 2020-08-04 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20200725_1743'),
        ('zarinpal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymenttransaction',
            options={'verbose_name': ['لیست تراکنش'], 'verbose_name_plural': ['لیست تراکنش ها']},
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='food_trans',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='food.FoodTransaction'),
        ),
    ]