# Generated by Django 2.0 on 2018-04-03 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20180403_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facility',
            old_name='faility_type',
            new_name='facility_type',
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
    ]
