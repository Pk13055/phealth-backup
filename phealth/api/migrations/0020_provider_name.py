# Generated by Django 2.0 on 2018-03-03 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20180301_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='name',
            field=models.CharField(default='Generic Hospital', max_length=100),
        ),
    ]