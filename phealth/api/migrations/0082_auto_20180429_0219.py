# Generated by Django 2.0 on 2018-04-28 20:49

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_auto_20180421_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcheckup',
            name='age',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(default=(0, None)),
        ),
        migrations.AddField(
            model_name='healthcheckup',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('both', 'both')], default='both', max_length=5),
        ),
        migrations.AddField(
            model_name='healthcheckup',
            name='type',
            field=models.CharField(choices=[('preventive', 'preventive'), ('diabetes', 'diabetes'), ('cancer', 'cancer'), ('antenatal', 'antenatal'), ('other', 'other')], default='preventive', max_length=35),
        ),
        migrations.AlterField(
            model_name='clinician',
            name='language',
            field=models.CharField(choices=[('hindi', 'Hindi'), ('english', 'English'), ('bengali', 'Bengali'), ('telugu', 'Telugu'), ('marathi', 'Marathi'), ('tamil', 'Tamil'), ('urdu', 'Urdu'), ('kannada', 'Kannada'), ('gujarati', 'Gujarati'), ('bhojpuri', 'Bhojpuri'), ('odia', 'Odia'), ('malayalam', 'Malayalam'), ('sanskri', 'Sanskri'), ('other', 'other')], default='other', max_length=100),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
    ]
