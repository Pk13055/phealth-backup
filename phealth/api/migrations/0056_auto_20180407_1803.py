# Generated by Django 2.0 on 2018-04-07 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20180407_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seeker',
            name='dob',
        ),


    ]
