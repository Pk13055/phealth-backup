# Generated by Django 2.0 on 2018-02-13 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180214_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='org_type',
            field=models.CharField(choices=[('corporate', 'Corporations'), ('college', 'Educational Institutions'), ('ngo', 'Non-government Organizations'), ('community', 'Gated communities')], default='corporate', max_length=100),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='org_size',
            field=models.CharField(choices=[('50-100', '50-100'), ('100-500', '100-500'), ('500-1000', '500-1000'), ('1000-5000', '1000-5000'), ('5000-10000', '5000-10000'), ('10000+', '10000+')], default='50-100', max_length=30),
        ),
    ]
