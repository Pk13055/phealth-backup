# Generated by Django 2.0 on 2018-04-05 08:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20180403_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familymember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='HealthProviderPlans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.PositiveSmallIntegerField(default=0)),
                ('amount_credit', models.PositiveSmallIntegerField(default=0)),
                ('image', models.ImageField(default='default_healthprovider_plan.jpg', upload_to='plans')),
                ('description', models.TextField()),
                ('first_consultation_share', models.PositiveSmallIntegerField(default=0)),
                ('subsequent_consultation_share', models.PositiveSmallIntegerField(default=0)),
                ('first_consultation_discount', models.PositiveSmallIntegerField(default=0)),
                ('subsequent_consultation_discount', models.PositiveSmallIntegerField(default=0)),
                ('validity', models.CharField(choices=[('6', '6 Months'), ('12', '12 Months'), ('24', '24 Months'), ('36', '36 Months')], default=0, max_length=200)),
                ('software_licence', models.CharField(choices=[('12', '12 Months'), ('24', '24 Months'), ('36', '36 Months')], default=0, max_length=200)),
                ('applicability', models.CharField(choices=[('12', '12 Months'), ('24', '24 Months'), ('36', '36 Months')], default=0, max_length=200)),
                ('coupon', models.ManyToManyField(blank=True, null=True, to='api.Provider')),
                ('service_provider', models.ManyToManyField(blank=True, null=True, to='api.User')),
                ('speciality_group', models.ManyToManyField(to='api.Group')),
            ],
        ),
        migrations.CreateModel(
            name='IdConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affix', models.CharField(blank=True, max_length=200, null=True)),
                ('prefix', models.CharField(blank=True, max_length=200, null=True)),
                ('tablename', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subrole', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Timesession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('fromtime', models.TimeField(blank=True, null=True)),
                ('totime', models.TimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='discountcard',
            name='applicability',
            field=models.CharField(choices=[('0', 'General'), ('1', 'Group/ Sponsored')], default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='coupon',
            field=models.ManyToManyField(blank=True, null=True, to='api.Coupon'),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='coverage',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='group_or_sponsor',
            field=models.ManyToManyField(blank=True, null=True, to='api.User'),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='image',
            field=models.ImageField(default='default_discountcatd.jpg', upload_to='discountcard'),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='price_extra_member',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='restriction',
            field=models.CharField(choices=[('0', 'No'), ('1', 'Yes')], default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='healthcheckup',
            name='applicability',
            field=models.CharField(choices=[('0', 'General'), ('1', 'Group/ Sponsored')], default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='healthcheckup',
            name='coupon',
            field=models.ManyToManyField(blank=True, null=True, to='api.Coupon'),
        ),
        migrations.AddField(
            model_name='healthcheckup',
            name='group_or_sponsor',
            field=models.ManyToManyField(blank=True, null=True, to='api.User'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FacilityType'),
        ),
        migrations.AlterField(
            model_name='healthcheckup',
            name='image',
            field=models.ImageField(default='default_healthcheck.jpg', upload_to='health_checks'),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='applicable_family_members',
            field=models.ManyToManyField(blank=True, null=True, to='api.Familymember'),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='extra_family_members',
            field=models.ManyToManyField(blank=True, null=True, related_name='extra_family_members', to='api.Familymember'),
        ),
    ]