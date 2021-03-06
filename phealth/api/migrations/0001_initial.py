# Generated by Django 2.0 on 2018-02-13 13:47

import api.models
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('pincode', models.CharField(max_length=9)),
                ('extra', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'address',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_on', models.DateTimeField(default=api.models.current_timestamp)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('code', models.IntegerField(unique=True)),
            ],
            options={
                'db_table': 'cities',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Clinician',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('work_timings', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), size=2), size=7)),
                ('break_timings', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), size=2), size=7)),
                ('vacations', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), size=2), size=None)),
                ('education', models.TextField()),
                ('experience', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
            ],
            options={
                'db_table': 'clinicians',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.IntegerField(unique=True)),
            ],
            options={
                'db_table': 'countries',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('validty', models.BooleanField(default=True)),
                ('expiry', models.DateField()),
                ('date_added', models.DateTimeField(default=api.models.current_timestamp, editable=False)),
            ],
            options={
                'db_table': 'coupons',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DiscountCard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
                ('price', models.PositiveSmallIntegerField(default=0)),
                ('validity', models.DateField()),
            ],
            options={
                'db_table': 'discountcards',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('code', models.IntegerField(unique=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.City')),
            ],
            options={
                'db_table': 'districts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HealthCheckup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40, unique=True)),
                ('description', models.TextField()),
                ('price', models.PositiveSmallIntegerField(default=0)),
                ('image', models.ImageField(upload_to='health_checks')),
            ],
            options={
                'db_table': 'healthchecks',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_branch', models.BooleanField(default=False)),
                ('active_from', models.DateField()),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Address')),
                ('clinicians', models.ManyToManyField(to='api.Clinician')),
                ('parent_provider', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Provider')),
            ],
            options={
                'db_table': 'providers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'questions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Reseller',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'resellers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SalesAgent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resellers', models.ManyToManyField(to='api.Reseller')),
            ],
            options={
                'db_table': 'salesagents',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Seeker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('profession', models.CharField(choices=[('doctor', 'doctor'), ('teacher', 'teacher'), ('engineer', 'engineer'), ('professor', 'professor'), ('business', 'business'), ('other', 'other')], max_length=100)),
                ('language', models.CharField(choices=[('english', 'english'), ('hindi', 'hindi'), ('telugu', 'telugu'), ('marathi', 'marathi'), ('malayalam', 'malayalam'), ('gujarati', 'gujarati'), ('bhojpuri', 'bhojpuri'), ('tamil', 'tamil'), ('other', 'other')], max_length=100)),
                ('dob', models.DateField()),
                ('profile_pic', models.ImageField(default='default_profile.jpg', upload_to='profile_pics')),
                ('family', models.ManyToManyField(related_name='_seeker_family_+', to='api.Seeker')),
            ],
            options={
                'db_table': 'seekers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'specialities',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('org_name', models.CharField(max_length=50)),
                ('org_size', models.PositiveSmallIntegerField(default=10)),
            ],
            options={
                'db_table': 'sponsors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('code', models.IntegerField(unique=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Country')),
            ],
            options={
                'db_table': 'states',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=70)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'tests',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TestCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'test_categories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('date_added', models.DateTimeField(default=api.models.current_timestamp)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Seeker')),
            ],
            options={
                'db_table': 'testimonials',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TestSubcategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.TestCategory')),
            ],
            options={
                'db_table': 'test_subcategories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('IP', models.GenericIPAddressField(editable=False)),
                ('timestamp', models.DateTimeField(default=api.models.current_timestamp, editable=False)),
                ('amount', models.PositiveSmallIntegerField(default=0)),
                ('status', models.CharField(choices=[('1', 'Paid to Pheatlh'), ('2', 'Paid to user'), ('3', 'Pending'), ('4', 'Failed')], max_length=1)),
            ],
            options={
                'db_table': 'transactions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.NullBooleanField(default=True, editable=False)),
                ('role', models.CharField(choices=[('healthprovider', 'healthprovider'), ('healthseeker', 'healthseeker'), ('clinician', 'clinician'), ('sponsor', 'sponsor'), ('salesagent', 'salesagent'), ('reseller', 'reseller'), ('admin', 'admin')], editable=False, max_length=30)),
                ('reg_date', models.DateTimeField(default=api.models.current_timestamp, editable=False)),
                ('last_update', models.DateTimeField(editable=False)),
                ('last_IP', models.GenericIPAddressField(editable=False)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=150)),
                ('mobile', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid Number', regex='^(\\+\\d{1,3}[- ]?)?\\d{10}$')])),
                ('password', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('answer', models.CharField(max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Question')),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='received', to='api.User'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issued', to='api.User'),
        ),
        migrations.AddField(
            model_name='test',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.TestSubcategory'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.User'),
        ),
        migrations.AddField(
            model_name='seeker',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.User'),
        ),
        migrations.AddField(
            model_name='salesagent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.User'),
        ),
        migrations.AddField(
            model_name='reseller',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.User'),
        ),
        migrations.AddField(
            model_name='provider',
            name='poc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.User'),
        ),
        migrations.AddField(
            model_name='provider',
            name='specialities',
            field=models.ManyToManyField(to='api.Speciality'),
        ),
        migrations.AddField(
            model_name='healthcheckup',
            name='tests',
            field=models.ManyToManyField(to='api.Test'),
        ),
        migrations.AddField(
            model_name='discountcard',
            name='health_checkups',
            field=models.ManyToManyField(to='api.HealthCheckup'),
        ),
        migrations.AddField(
            model_name='clinician',
            name='specialities',
            field=models.ManyToManyField(to='api.Speciality'),
        ),
        migrations.AddField(
            model_name='clinician',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.User'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.State'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='provider',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Provider'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='under',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Clinician'),
        ),
        migrations.AddField(
            model_name='address',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.District'),
        ),
    ]
