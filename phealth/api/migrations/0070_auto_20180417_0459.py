# Generated by Django 2.0 on 2018-04-16 23:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_auto_20180417_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
        migrations.AlterField(
            model_name='location',
            name='address_component',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[{'long_name': '', 'short_name': '', 'types': []}, {'long_name': '', 'short_name': '', 'types': []}, {'long_name': '', 'short_name': '', 'types': []}, {'long_name': '', 'short_name': '', 'types': []}, {'long_name': '', 'short_name': '', 'types': []}, {'long_name': '', 'short_name': '', 'types': []}, {'long_name': '', 'short_name': '', 'types': []}], editable=False, verbose_name=django.contrib.postgres.fields.jsonb.JSONField()),
        ),
    ]