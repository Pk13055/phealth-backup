# Generated by Django 2.0 on 2018-03-28 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20180328_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Address'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='poc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.User'),
        ),
    ]
