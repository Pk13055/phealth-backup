# Generated by Django 2.0 on 2018-02-25 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20180225_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='clicks',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
