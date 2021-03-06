# Generated by Django 2.0 on 2018-05-18 06:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_auto_20180517_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='testcategory',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Test'),
        ),
        
        migrations.AlterField(
            model_name='testsubcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TestCategory'),
        ),
    ]
