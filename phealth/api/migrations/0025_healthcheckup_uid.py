# Generated by Django 2.0 on 2018-03-11 11:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20180311_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcheckup',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
