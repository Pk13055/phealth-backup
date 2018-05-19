# Generated by Django 2.0 on 2018-05-12 01:29

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0093_auto_20180511_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('medication', 'medication'), ('checkup', 'checkup'), ('appointment', 'appointment'), ('consultation', 'consultation'), ('other', 'other')], default='consultation', max_length=40)),
                ('method', models.CharField(default='mobile', max_length=15)),
                ('duration', django.contrib.postgres.fields.ranges.DateRangeField()),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Seeker')),
            ],
            options={
                'db_table': 'alerts',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
    ]
