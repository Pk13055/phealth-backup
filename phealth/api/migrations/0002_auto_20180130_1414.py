# Generated by Django 2.0 on 2018-01-30 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='agegroup',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='alertsources',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='alerttype',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='appointmentbooking',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='availablefacilities',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='bookingsources',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='businessregtype',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='clinicianmemberships',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='clinicians',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='cliniciansdates',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='clinicianseducation',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='cliniciansexperience',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='cliniciansspeciality',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='conditions',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='couponaccept',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='coupons',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='designation',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='discountcard',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='discountcardfamily',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='discountcardfamilyextra',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='facilities',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='facilitiesservices',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='family',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='gender',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthcheckbooking',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthchecks',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthchecksinclusion',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthproviders',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthprovidersspeciality',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthrecords',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthseeker',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthseekeralerts',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthseekeravailabilities',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthseekerhealthrecords',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='healthseekertype',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='interest',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='languages',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='photoalbum',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='plans',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='plansgroups',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='plansgroupsspecialities',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='priyority',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='profession',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='qualification',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='referrels',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='referrelscheme',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='registrationwelcomemessage',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='resellerpackages',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='resellers',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='salesagentpackages',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='salesagents',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='salestarget',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='secretquestions',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='speciality',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='specialitytype',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='sponsors',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='sponsorsgroup',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='symptoms',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='telephone',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='testcategory',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='testimonials',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='testsubcategory',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='timeslots',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='trxnappointmentbookings',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='trxncoupons',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='trxndiscountcard',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='trxnhealthcheckbooking',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='trxnpayments',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='week',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='wellnessplan',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='wellnessplanprofession',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='wellnessplansocialhistory',
            options={'managed': True},
        ),
    ]
