# Generated by Django 2.0 on 2018-03-28 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20180328_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speciality',
            name='description',
        ),
        migrations.RemoveField(
            model_name='speciality',
            name='name',
        ),
    ]