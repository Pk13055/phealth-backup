# Generated by Django 2.0 on 2018-02-15 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180214_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='users',
            field=models.ManyToManyField(to='api.Seeker'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
