# Generated by Django 2.0 on 2018-05-14 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_auto_20180514_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
    ]