# Generated by Django 2.0 on 2018-01-30 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180130_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='agegroup',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='alertsources',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='alerttype',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='appointmentbooking',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='availablefacilities',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='bookingsources',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='businessregtype',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='clinicianmemberships',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='clinicians',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='cliniciansdates',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='clinicianseducation',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='cliniciansexperience',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='cliniciansspeciality',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='conditions',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='couponaccept',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='coupons',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='designation',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='discountcard',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='discountcardfamily',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='discountcardfamilyextra',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='facilities',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='facilitiesservices',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='family',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='gender',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthcheckbooking',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthchecks',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthchecksinclusion',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthproviders',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthprovidersspeciality',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthrecords',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthseeker',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthseekeralerts',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthseekeravailabilities',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthseekerhealthrecords',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='healthseekertype',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='interest',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='languages',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='photoalbum',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='plans',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='plansgroups',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='plansgroupsspecialities',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='priyority',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='profession',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='qualification',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='referrels',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='referrelscheme',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='registrationwelcomemessage',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='resellerpackages',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='resellers',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='salesagentpackages',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='salesagents',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='salestarget',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='secretquestions',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='speciality',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='specialitytype',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='sponsors',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='sponsorsgroup',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='symptoms',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='telephone',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='testcategory',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='testimonials',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='testsubcategory',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='timeslots',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='trxnappointmentbookings',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='trxncoupons',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='trxndiscountcard',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='trxnhealthcheckbooking',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='trxnpayments',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='week',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='wellnessplan',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='wellnessplanprofession',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='wellnessplansocialhistory',
            options={'managed': False},
        ),
    ]
