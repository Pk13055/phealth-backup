# Generated by Django 2.0 on 2018-04-03 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20180403_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='faility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
    ]