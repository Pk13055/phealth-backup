# Generated by Django 2.0 on 2018-02-25 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20180225_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='featured_posts',
            field=models.ManyToManyField(to='api.Post'),
        ),
        migrations.AddField(
            model_name='cdn',
            name='code',
            field=models.CharField(default='misc', max_length=30),
        ),
    ]
