# Generated by Django 2.0 on 2018-04-21 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0080_auto_20180419_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='seeker',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Location'),
        ),
 
    ]