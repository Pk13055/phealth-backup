# Generated by Django 2.0 on 2018-03-21 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20180321_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='duration',
            field=models.PositiveIntegerField(default=30),
        ),
    ]
