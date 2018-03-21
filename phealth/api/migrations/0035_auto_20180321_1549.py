# Generated by Django 2.0 on 2018-03-21 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_calendarevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='css_class',
            field=models.CharField(blank=True, choices=[('event-info', 'Info'), ('event-success', 'Success'), ('event-warning', 'Warning'), ('event-special', 'Special')], editable=False, max_length=20, verbose_name='CSS Class'),
        ),
    ]
