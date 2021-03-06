# Generated by Django 2.0 on 2018-02-16 07:13

from django.contrib.postgres.operations import HStoreExtension
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180216_0125'),
    ]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name='discountcard',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='reseller',
            name='discount_cards',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='salesagent',
            name='discount_cards',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to='api.Seeker'),
        ),
    ]
