# Generated by Django 3.0.6 on 2020-07-28 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TodoApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoapp',
            name='date',
            field=models.TimeField(),
        ),
    ]