# Generated by Django 2.0 on 2018-04-12 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_auto_20180412_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
    ]