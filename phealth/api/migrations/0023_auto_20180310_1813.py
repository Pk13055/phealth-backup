# Generated by Django 2.0 on 2018-03-10 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_sponsor_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Address'),
        ),
    ]