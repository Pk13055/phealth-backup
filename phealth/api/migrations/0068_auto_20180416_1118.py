# Generated by Django 2.0 on 2018-04-16 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_auto_20180416_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='seeker',
            name='language',
            field=models.CharField(choices=[('english', 'english'), ('hindi', 'hindi'), ('telugu', 'telugu'), ('marathi', 'marathi'), ('malayalam', 'malayalam'), ('gujarati', 'gujarati'), ('bhojpuri', 'bhojpuri'), ('tamil', 'tamil'), ('other', 'other')], default='english', max_length=100),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
    ]
