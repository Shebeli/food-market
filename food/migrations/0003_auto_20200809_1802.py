# Generated by Django 3.0.6 on 2020-08-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20200725_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thefood',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='food_pics'),
        ),
    ]
