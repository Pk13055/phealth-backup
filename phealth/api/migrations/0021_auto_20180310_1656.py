# Generated by Django 2.0 on 2018-03-10 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_provider_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('size', models.CharField(choices=[('50-100', '50-100'), ('100-500', '100-500'), ('500-1000', '500-1000'), ('1000-5000', '1000-5000'), ('5000-10000', '5000-10000'), ('10000+', '10000+')], default='50-100', max_length=30)),
                ('type', models.CharField(choices=[('corporate', 'Corporations'), ('college', 'Educational Institutions'), ('ngo', 'Non-government Organizations'), ('community', 'Gated communities')], default='corporate', max_length=100)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Address')),
            ],
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='org_name',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='org_size',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='org_type',
        ),
        migrations.AddField(
            model_name='sponsor',
            name='pocs',
            field=models.ManyToManyField(blank=True, null=True, related_name='pocs', to='api.User'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='poc', to='api.User'),
        ),
    ]
