# Generated by Django 2.0 on 2018-03-21 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20180321_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendarevent',
            name='appointment_ptr',
        ),
        migrations.DeleteModel(
            name='CalendarEvent',
        ),
    ]
