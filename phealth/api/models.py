# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import hashlib

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    district = models.ForeignKey('District', models.DO_NOTHING)
    country = models.ForeignKey('Country', models.DO_NOTHING)
    state = models.ForeignKey('State', models.DO_NOTHING)
    city = models.ForeignKey('City', models.DO_NOTHING)
    latlong = models.CharField(max_length=225, blank=True, null=True)
    doorno = models.CharField(max_length=225, blank=True, null=True)
    landmark = models.CharField(max_length=225, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    fax = models.CharField(max_length=225, blank=True, null=True)
    contactperson = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.district) + " "  + str(self.state) + " " + str(self.city)

    class Meta:
        managed = False
        db_table = 'address'


class Agegroup(models.Model):
    agegroup_id = models.AutoField(primary_key=True)
    agegroup = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.agegroup)

    class Meta:
        managed = False
        db_table = 'agegroup'


class Alertsources(models.Model):
    alertsources_id = models.AutoField(primary_key=True)
    alertsource = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.alertsource)

    class Meta:
        managed = False
        db_table = 'alertsources'


class Alerttype(models.Model):
    alerttype_id = models.AutoField(primary_key=True)
    alerttype = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.alerttype)

    class Meta:
        managed = False
        db_table = 'alerttype'


class Appointmentbooking(models.Model):
    appointmentbooking_id = models.AutoField(primary_key=True)
    date = models.DateField()
    priyority = models.ForeignKey('Priyority', models.DO_NOTHING)
    speciality = models.ForeignKey('Speciality', models.DO_NOTHING)
    healthseeker = models.ForeignKey('Healthseeker', models.DO_NOTHING)
    clinicians = models.ForeignKey('Clinicians', models.DO_NOTHING)
    bookingsources = models.ForeignKey('Bookingsources', models.DO_NOTHING)
    time = models.TimeField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    ipaddress = models.CharField(max_length=225, blank=True, null=True)
    macaddress = models.CharField(max_length=225, blank=True, null=True)
    isnew = models.IntegerField(blank=True, null=True)
    visittype = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        managed = False
        db_table = 'appointmentbooking'
        unique_together = (('appointmentbooking_id', 'date'),)


class Availablefacilities(models.Model):
    availablefacilities_id = models.AutoField(primary_key=True)
    facilities_services = models.ForeignKey('FacilitiesServices', models.DO_NOTHING)
    healthproviders = models.ForeignKey('Healthproviders', models.DO_NOTHING)
    facilities = models.ForeignKey('Facilities', models.DO_NOTHING)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.facilities)

    class Meta:
        managed = False
        db_table = 'availablefacilities'


class Bookingsources(models.Model):
    bookingsources_id = models.AutoField(primary_key=True)
    sourcename = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.sourcename)

    class Meta:
        managed = False
        db_table = 'bookingsources'


class Businessregtype(models.Model):
    businessregtype_id = models.AutoField(primary_key=True)
    businessregtype = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.businessregtype)

    class Meta:
        managed = False
        db_table = 'businessregtype'


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=225)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.city)

    class Meta:
        managed = False
        db_table = 'city'


class ClinicianMemberships(models.Model):
    clinician_memberships_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, models.DO_NOTHING)
    country = models.ForeignKey('Country', models.DO_NOTHING)
    association = models.CharField(max_length=225, blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.association)

    def save(self, *args, **kwargs):
        if self.reg_date == "" or self.reg_date is None:
            self.reg_date = datetime.datetime.now().isoformat('T')
        super(ClinicianMemberships, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'clinician_memberships'


class Clinicians(models.Model):
    clinicians_id = models.AutoField(primary_key=True)
    languages = models.ForeignKey('Languages', models.DO_NOTHING)
    gender = models.ForeignKey('Gender', models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    dob = models.DateField(blank=True, null=True)
    # fee = models.IntegerField(blank=True, null=False, default=0)
    image = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.users)

    class Meta:
        managed = False
        db_table = 'clinicians'


class CliniciansDates(models.Model):
    clinicians_dates_id = models.AutoField(primary_key=True)
    clinicians = models.ForeignKey(Clinicians, models.DO_NOTHING)
    timeslots = models.ForeignKey('Timeslots', models.DO_NOTHING)
    week = models.ForeignKey('Week', models.DO_NOTHING)
    alldays = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.timeslots)

    class Meta:
        managed = False
        db_table = 'clinicians_dates'


class CliniciansEducation(models.Model):
    clinicians_education_id = models.AutoField(primary_key=True)
    qualification = models.ForeignKey('Qualification', models.DO_NOTHING)
    clinicians = models.ForeignKey(Clinicians, models.DO_NOTHING)
    registrationno = models.CharField(max_length=225, blank=True, null=True)
    college = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.qualification)

    class Meta:
        managed = False
        db_table = 'clinicians_education'


class CliniciansExperience(models.Model):
    clinicians_experience_id = models.AutoField(primary_key=True)
    designation = models.ForeignKey('Designation', models.DO_NOTHING)
    clinicians = models.ForeignKey(Clinicians, models.DO_NOTHING)
    institution = models.CharField(max_length=225, blank=True, null=True)
    workfrom = models.DateField(blank=True, null=True)
    workto = models.DateField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.institution)

    def save(self, *args, **kwargs):
        if self.reg_date == "" or self.reg_date is None:
            self.reg_date = datetime.datetime.now()
        super(CliniciansExperience, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'clinicians_experience'


class CliniciansSpeciality(models.Model):
    clinicians_speciality_id = models.AutoField(primary_key=True)
    symptoms = models.ForeignKey('Symptoms', models.DO_NOTHING)
    clinicians = models.ForeignKey(Clinicians, models.DO_NOTHING)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.healthproviders_speciality)

    def save(self, *args, **kwargs):
        if self.reg_date == "" or self.reg_date is None:
            self.reg_date = datetime.datetime.now()
        super(CliniciansSpeciality, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'clinicians_speciality'


class Conditions(models.Model):
    conditions_id = models.AutoField(primary_key=True)
    conditionname = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.conditionname)

    class Meta:
        managed = False
        db_table = 'conditions'


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.country)

    class Meta:
        managed = False
        db_table = 'country'


class Couponaccept(models.Model):
    couponaccept_id = models.AutoField(primary_key=True)
    couponaccept = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.couponaccept)

    class Meta:
        managed = False
        db_table = 'couponaccept'


class Coupons(models.Model):
    coupons_id = models.AutoField(primary_key=True)
    coupon = models.CharField(max_length=225, blank=True, null=True)
    applicablesponsor = models.IntegerField(blank=True, null=True)
    uniquecode = models.CharField(max_length=225, blank=True, null=True)
    validity = models.DateField(blank=True, null=True)
    timevalidity = models.IntegerField(blank=True, null=True)
    couponstatus = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupons'

    def save(self, *args, **kwargs):
        try:
            self.couponstatus = int(self.couponstatus)
        except:
            self.couponstatus = 0
        self.uniquecode = hashlib.sha1(
            datetime.datetime.now().isoformat('T').encode('utf-8')).hexdigest()
        print(self)
        super(Coupons, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.coupon)



class Designation(models.Model):
    designation_id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.designation)

    class Meta:
        managed = False
        db_table = 'designation'


class Discountcard(models.Model):
    '''
        `added by the admin given to
            - user directly (has to buy)
            - Sponsor (n users * cost)
    '''

    discountcard_id = models.AutoField(primary_key=True)
    healthchecks = models.ForeignKey('Healthchecks', models.DO_NOTHING)
    discountcard = models.CharField(max_length=225, blank=True, null=True)
    description = models.CharField(max_length=225, blank=True, null=True)
    eligibility = models.IntegerField(blank=True, null=True)
    familyrestriction = models.IntegerField(blank=True, null=True)
    addfamilyrestriction = models.IntegerField(blank=True, null=True)
    applicablesponser = models.IntegerField(blank=True, null=True)
    otherbenfits = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.discountcard)

    class Meta:
        managed = False
        db_table = 'discountcard'


class DiscountcardFamily(models.Model):
    discountcard_family_id = models.AutoField(primary_key=True)
    discountcard = models.ForeignKey(Discountcard, models.DO_NOTHING)
    family = models.ForeignKey('Family', models.DO_NOTHING)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.family) + " : " + self.price

    class Meta:
        managed = False
        db_table = 'discountcard_family'


class DiscountcardFamilyExtra(models.Model):
    discountcard_family_extra_id = models.AutoField(primary_key=True)
    family = models.ForeignKey('Family', models.DO_NOTHING)
    discountcard = models.ForeignKey(Discountcard, models.DO_NOTHING)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discountcard_family_extra'


class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.district)

    class Meta:
        managed = False
        db_table = 'district'


class Facilities(models.Model):
    facilities_id = models.AutoField(primary_key=True)
    facility = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.facility)

    class Meta:
        managed = False
        db_table = 'facilities'


class FacilitiesServices(models.Model):
    facilities_services_id = models.AutoField(primary_key=True)
    facilities = models.ForeignKey(Facilities, models.DO_NOTHING)
    facilities_services = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.facilities_services)

    class Meta:
        managed = False
        db_table = 'facilities_services'


class Family(models.Model):
    family_id = models.AutoField(primary_key=True)
    family = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.family)

    class Meta:
        managed = False
        db_table = 'family'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    users_feedback = models.CharField(max_length=225, blank=True, null=True)
    from_2 = models.CharField(max_length=225, blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    feedbackstatus = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.users_feedback)

    class Meta:
        managed = False
        db_table = 'feedback'


class Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.gender)

    class Meta:
        managed = False
        db_table = 'gender'


class Healthcheckbooking(models.Model):
    healthcheckbooking_id = models.AutoField(primary_key=True)
    healthseeker = models.ForeignKey('Healthseeker', models.DO_NOTHING)
    healthproviders = models.ForeignKey('Healthproviders', models.DO_NOTHING)
    bookingsources = models.ForeignKey(Bookingsources, models.DO_NOTHING)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        managed = False
        db_table = 'healthcheckbooking'


class Healthchecks(models.Model):
    healthchecks_id = models.AutoField(primary_key=True)
    coupons = models.ForeignKey(Coupons, models.DO_NOTHING)
    healthcheck = models.CharField(max_length=225, blank=True, null=True)
    description = models.CharField(max_length=225, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    promoimage = models.CharField(max_length=225, blank=True, null=True)
    applicable_sponser = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.healthcheck)

    class Meta:
        managed = False
        db_table = 'healthchecks'


class HealthchecksInclusion(models.Model):
    healthchecks_inclusion_id = models.AutoField(primary_key=True)
    test = models.ForeignKey('Test', models.DO_NOTHING)
    healthchecks = models.ForeignKey(Healthchecks, models.DO_NOTHING)

    def __str__(self):
        return str(self.healthchecks)

    class Meta:
        managed = False
        db_table = 'healthchecks_inclusion'


class Healthproviders(models.Model):
    healthproviders_id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    is_branch = models.IntegerField(blank=True, null=True)
    under_healthproviders_id = models.IntegerField(blank=True, null=True)
    display_cost = models.IntegerField(blank=True, null=True)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)
    m_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.users)

    class Meta:
        managed = False
        db_table = 'healthproviders'


class HealthprovidersSpeciality(models.Model):
    healthproviders_speciality_id = models.AutoField(primary_key=True)
    speciality = models.ForeignKey('Speciality', models.DO_NOTHING)
    healthproviders = models.ForeignKey(Healthproviders, models.DO_NOTHING)
    sort_by = models.IntegerField(blank=True, null=True)
    speciality_name = models.CharField(max_length=225, blank=True, null=True)
    speciality_description = models.CharField(max_length=225, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    discountpercentage = models.IntegerField(blank=True, null=True)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.speciality_name)

    class Meta:
        managed = False
        db_table = 'healthproviders_speciality'


class Healthrecords(models.Model):
    healthrecords_id = models.AutoField(primary_key=True)
    healthrecord = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.healthrecord)

    class Meta:
        managed = False
        db_table = 'healthrecords'


class Healthseeker(models.Model):
    healthseeker_id = models.AutoField(primary_key=True)
    healthseeker_type = models.ForeignKey('HealthseekerType', models.DO_NOTHING)
    profession = models.ForeignKey('Profession', models.DO_NOTHING)
    languages = models.ForeignKey('Languages', models.DO_NOTHING)
    gender = models.ForeignKey(Gender, models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    underfamily = models.IntegerField(blank=True, null=True)
    undersponser = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    image = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.users)

    class Meta:
        managed = False
        db_table = 'healthseeker'


class HealthseekerAlerts(models.Model):
    healthseeker_alerts_id = models.AutoField(primary_key=True)
    alertsources = models.ForeignKey(Alertsources, models.DO_NOTHING)
    alerttype = models.ForeignKey(Alerttype, models.DO_NOTHING)
    healthseeker = models.ForeignKey(Healthseeker, models.DO_NOTHING)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)
    alert_to = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Healthseeker : " + str(self.alertsources)

    class Meta:
        managed = False
        db_table = 'healthseeker_alerts'


class HealthseekerAvailabilities(models.Model):
    healthseeker_availabilities_id = models.AutoField(primary_key=True)
    healthchecks = models.ForeignKey(Healthchecks, models.DO_NOTHING)
    discountcard = models.ForeignKey(Discountcard, models.DO_NOTHING)
    coupons = models.ForeignKey(Coupons, models.DO_NOTHING)
    healthseeker = models.ForeignKey(Healthseeker, models.DO_NOTHING)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.coupons)

    class Meta:
        managed = False
        db_table = 'healthseeker_availabilities'


class HealthseekerHealthrecords(models.Model):
    healthseeker_healthrecords_id = models.AutoField(primary_key=True)
    healthrecords = models.ForeignKey(Healthrecords, models.DO_NOTHING)
    healthseeker = models.ForeignKey(Healthseeker, models.DO_NOTHING)
    refdate = models.DateField(blank=True, null=True)
    file_2 = models.CharField(max_length=225, blank=True, null=True)
    file3 = models.CharField(max_length=225, blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    m_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.healthrecords)

    class Meta:
        managed = False
        db_table = 'healthseeker_healthrecords'


class HealthseekerType(models.Model):
    healthseeker_type_id = models.AutoField(primary_key=True)
    healthseeker_type = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.healthseeker_type)

    class Meta:
        managed = False
        db_table = 'healthseeker_type'


class Interest(models.Model):
    interest_id = models.AutoField(primary_key=True)
    healthseeker = models.ForeignKey(Healthseeker, models.DO_NOTHING)
    interest = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.interest)

    class Meta:
        managed = False
        db_table = 'interest'


class Languages(models.Model):
    languages_id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.language)

    class Meta:
        managed = False
        db_table = 'languages'


class Photoalbum(models.Model):
    photoalbum_id = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    photo_title = models.CharField(max_length=225, blank=True, null=True)
    image_path = models.CharField(max_length=225)
    forusage = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.photo_title)

    class Meta:
        managed = False
        db_table = 'photoalbum'


class Plans(models.Model):
    plans_id = models.AutoField(primary_key=True)
    plans_groups = models.ForeignKey('PlansGroups', models.DO_NOTHING)
    plan = models.CharField(max_length=225, blank=True, null=True)
    description = models.CharField(max_length=225, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    noofpatients = models.IntegerField(blank=True, null=True)
    benefits = models.CharField(max_length=225, blank=True, null=True)
    share1stconsultation = models.IntegerField(blank=True, null=True)
    sharenextconsultation = models.IntegerField(blank=True, null=True)
    planworks = models.CharField(max_length=225, blank=True, null=True)
    addbenfits = models.CharField(max_length=225, blank=True, null=True)
    cmslicencevalidity = models.CharField(max_length=225, blank=True, null=True)
    validity = models.CharField(max_length=225, blank=True, null=True)
    discount1stconsultation = models.IntegerField(blank=True, null=True)
    discountnextconsultation = models.IntegerField(blank=True, null=True)
    promoimage = models.CharField(max_length=225, blank=True, null=True)
    applicability = models.CharField(max_length=225, blank=True, null=True)
    doctorscoupon = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.plan)

    class Meta:
        managed = False
        db_table = 'plans'


class PlansGroups(models.Model):
    plans_groups_id = models.AutoField(primary_key=True)
    plans_groups_specialities = models.ForeignKey('PlansGroupsSpecialities', models.DO_NOTHING)
    plans_group = models.CharField(max_length=225, blank=True, null=True)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.plans_group)

    class Meta:
        managed = False
        db_table = 'plans_groups'


class PlansGroupsSpecialities(models.Model):
    plans_groups_specialities_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'plans_groups_specialities'


class Priyority(models.Model):
    priyority_id = models.AutoField(primary_key=True)
    priyority = models.IntegerField(blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.priyority)

    class Meta:
        managed = False
        db_table = 'priyority'


class Profession(models.Model):
    profession_id = models.AutoField(primary_key=True)
    poorofession = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.poorofession)

    class Meta:
        managed = False
        db_table = 'profession'


class Qualification(models.Model):
    qualification_id = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.qualification)

    class Meta:
        managed = False
        db_table = 'qualification'


class Referrels(models.Model):
    referrels_id = models.AutoField(primary_key=True)
    fromusers_id = models.IntegerField(blank=True, null=True)
    referredusers_id = models.IntegerField(blank=True, null=True)
    cashback = models.IntegerField(blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.referral_id)

    class Meta:
        managed = False
        db_table = 'referrels'


class Referrelscheme(models.Model):
    referrelscheme_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=225, blank=True, null=True)
    noofreferels = models.IntegerField(blank=True, null=True)
    cashback = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        managed = False
        db_table = 'referrelscheme'


class RegistrationWelcomeMessage(models.Model):
    registration_welcome_message_id = models.AutoField(primary_key=True)
    registration_welcome_message = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)
    m_user = models.IntegerField(blank=True, null=True)
    c_user = models.IntegerField(blank=True, null=True)
    m_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.registration_welcome_message)

    class Meta:
        managed = False
        db_table = 'registration_welcome_message'


class Resellerpackages(models.Model):
    resellerpackages_id = models.AutoField(primary_key=True)
    salestarget = models.ForeignKey('Salestarget', models.DO_NOTHING)
    packagename = models.CharField(max_length=225, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    noofdiscountcards = models.IntegerField(blank=True, null=True)
    packagetype = models.CharField(max_length=225, blank=True, null=True)
    validity = models.IntegerField(blank=True, null=True)
    campaignvalidfrom = models.DateField(blank=True, null=True)
    campaignvalidto = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.packagename)

    class Meta:
        managed = False
        db_table = 'resellerpackages'


class Resellers(models.Model):
    resellers_id = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    fathername = models.CharField(max_length=225, blank=True, null=True)
    relationofsalesagents = models.CharField(max_length=225, blank=True, null=True)
    idproof = models.CharField(max_length=225, blank=True, null=True)
    serviceoffered = models.CharField(max_length=225, blank=True, null=True)
    seviceagreementimage = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.users)

    class Meta:
        managed = False
        db_table = 'resellers'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=225)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)
    roleocode = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.role)

    class Meta:
        managed = False
        db_table = 'role'


class Salesagentpackages(models.Model):
    salesagentpackages_id = models.AutoField(primary_key=True)
    salestarget = models.ForeignKey('Salestarget', models.DO_NOTHING)
    packagename = models.CharField(max_length=225, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    noofdiscountcards = models.IntegerField(blank=True, null=True)
    packagetype = models.CharField(max_length=225, blank=True, null=True)
    validity = models.IntegerField(blank=True, null=True)
    campaignvalidfrom = models.DateField(blank=True, null=True)
    campaignvalidto = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.packagename)

    class Meta:
        managed = False
        db_table = 'salesagentpackages'


class Salesagents(models.Model):
    salesagents_id = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    agencyname = models.CharField(max_length=225, blank=True, null=True)
    registrationdate = models.DateField(blank=True, null=True)
    registrationno = models.IntegerField(blank=True, null=True)
    registrationproof = models.CharField(max_length=225, blank=True, null=True)
    authorizedpersonproof = models.CharField(max_length=225, blank=True, null=True)
    serviceoffered = models.CharField(max_length=225, blank=True, null=True)
    minimumnoresellers = models.IntegerField(blank=True, null=True)
    serviceproposal = models.CharField(max_length=225, blank=True, null=True)
    ndaagreemert = models.IntegerField(blank=True, null=True)
    ndaagreementproof = models.CharField(max_length=225, blank=True, null=True)
    agreementstarts = models.DateField(blank=True, null=True)
    agreementends = models.DateField(blank=True, null=True)
    serviceagreementimage = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.agencyname + " " + str(self.users))

    class Meta:
        managed = False
        db_table = 'salesagents'


class Salestarget(models.Model):
    salestarget_id = models.AutoField(primary_key=True)
    salestarget = models.CharField(max_length=225, blank=True, null=True)
    noofsales = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    addextracards = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.salestarget)

    class Meta:
        managed = False
        db_table = 'salestarget'


class Secretquestions(models.Model):
    secretquestions_id = models.AutoField(primary_key=True)
    secretquestion = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.secretquestion)

    class Meta:
        managed = False
        db_table = 'secretquestions'


class Speciality(models.Model):
    speciality_id = models.AutoField(primary_key=True)
    speciality_type = models.ForeignKey('SpecialityType', models.DO_NOTHING)
    qualification = models.ForeignKey(Qualification, models.DO_NOTHING)
    speciality = models.CharField(max_length=225, blank=True, null=True, default="None")
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.speciality)

    class Meta:
        managed = False
        db_table = 'speciality'


class SpecialityType(models.Model):
    speciality_type_id = models.AutoField(primary_key=True)
    speciality_type_name = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.speciality_type_name)

    class Meta:
        managed = False
        db_table = 'speciality_type'


class Sponsors(models.Model):
    sponsors_id = models.AutoField(primary_key=True)
    sponsors_group = models.ForeignKey('SponsorsGroup', models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    businessregtype = models.ForeignKey(Businessregtype, models.DO_NOTHING)
    organizationname = models.CharField(max_length=225, blank=True, null=True)
    groupsize = models.IntegerField(blank=True, null=True)
    designation = models.CharField(max_length=225, blank=True, null=True)
    image = models.CharField(max_length=225, blank=True, null=True)
    operatinghours = models.CharField(max_length=225, blank=True, null=True)
    oprtainglocation = models.CharField(max_length=225, blank=True, null=True)
    website = models.CharField(max_length=225, blank=True, null=True)
    requiredlocation = models.CharField(max_length=225, blank=True, null=True)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.users)

    class Meta:
        managed = False
        db_table = 'sponsors'


class SponsorsGroup(models.Model):
    sponsors_group_id = models.AutoField(primary_key=True)
    sponsors_group = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.sponsors_group)

    class Meta:
        managed = False
        db_table = 'sponsors_group'


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.state)

    class Meta:
        managed = False
        db_table = 'state'


class Symptoms(models.Model):
    symptoms_id = models.AutoField(primary_key=True)
    symptoms = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.symptoms)

    class Meta:
        managed = True
        db_table = 'symptoms'


class Telephone(models.Model):
    telephone_id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    phone = models.IntegerField(blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        managed = False
        db_table = 'telephone'


class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_subcategory = models.ForeignKey('TestSubcategory', models.DO_NOTHING)
    test_category = models.ForeignKey('TestCategory', models.DO_NOTHING)
    test = models.CharField(max_length=225, blank=True, null=True)
    description = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class TestCategory(models.Model):
    test_category_id = models.AutoField(primary_key=True)
    test_category = models.CharField(max_length=225, blank=True, null=True)
    description = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_category'


class TestSubcategory(models.Model):
    test_subcategory_id = models.AutoField(primary_key=True)
    test_category = models.ForeignKey(TestCategory, models.DO_NOTHING)
    subcategory = models.CharField(max_length=225, blank=True, null=True)
    description = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_subcategory'


class Testimonials(models.Model):
    testimonials_id = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    testimonial = models.CharField(max_length=225, blank=True, null=True)
    image = models.CharField(max_length=225, blank=True, null=True)
    video = models.CharField(max_length=225, blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)
    activefrom = models.DateTimeField(blank=True, null=True)
    activeto = models.DateTimeField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.testimonial)

    class Meta:
        managed = False
        db_table = 'testimonials'


class Timeslots(models.Model):
    timeslots_id = models.AutoField(primary_key=True)
    timeslots = models.CharField(max_length=225, blank=True, null=True)
    fromslot = models.TimeField(blank=True, null=True)
    toslot = models.TimeField(blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.timeslots)

    class Meta:
        managed = False
        db_table = 'timeslots'


class TrxnAppointmentbookings(models.Model):
    trxn_appointmentbookings_id = models.AutoField(primary_key=True)
    appointmentbooking_date = models.DateField()
    appointmentbooking = models.ForeignKey(Appointmentbooking, models.DO_NOTHING)
    status_2 = models.CharField(max_length=225, blank=True, null=True)
    session_activity = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=225, blank=True, null=True)
    trxn_by = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.appointmentbooking)

    class Meta:
        managed = False
        db_table = 'trxn_appointmentbookings'


class TrxnCoupons(models.Model):
    trxn_coupons_id = models.AutoField(primary_key=True)
    coupons = models.ForeignKey(Coupons, models.DO_NOTHING)
    status_2 = models.CharField(max_length=225, blank=True, null=True)
    sessionactivity = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=225, blank=True, null=True)
    trxn_by = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.coupons)

    class Meta:
        managed = False
        db_table = 'trxn_coupons'


class TrxnDiscountcard(models.Model):
    trxn_discountcard_id = models.AutoField(primary_key=True)
    discountcard = models.ForeignKey(Discountcard, models.DO_NOTHING)
    status_2 = models.CharField(max_length=225, blank=True, null=True)
    sessionactivity = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=225, blank=True, null=True)
    trxn_by = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.discountcard)

    class Meta:
        managed = False
        db_table = 'trxn_discountcard'


class TrxnHealthcheckbooking(models.Model):
    trxn_healthcheckbooking_id = models.AutoField(primary_key=True)
    healthcheckbooking = models.ForeignKey(Healthcheckbooking, models.DO_NOTHING)
    status_2 = models.CharField(max_length=225, blank=True, null=True)
    sessionactivity = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=225, blank=True, null=True)
    trxn_by = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.healthcheckbooking)

    class Meta:
        managed = False
        db_table = 'trxn_healthcheckbooking'


class TrxnPayments(models.Model):
    trxn_payments_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=True, null=True)
    status_2 = models.CharField(max_length=225, blank=True, null=True)
    paymentfor = models.CharField(max_length=225, blank=True, null=True)
    for_id = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=225, blank=True, null=True)
    trxn_by = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.amount)

    class Meta:
        managed = False
        db_table = 'trxn_payments'


class Users(models.Model):
    users_id = models.AutoField(primary_key=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    secretquestions = models.ForeignKey(Secretquestions, models.DO_NOTHING, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, null=True)
    mobile = models.IntegerField(null=True)
    email = models.CharField(max_length=225)
    firstname = models.CharField(max_length=225, blank=True, null=True)
    lastname = models.CharField(max_length=225, blank=True, null=True)
    middlename = models.CharField(max_length=225, blank=True, null=True)
    enc_password = models.CharField(max_length=225)
    verified = models.IntegerField(blank=True, null=True)
    pw_request = models.IntegerField(blank=True, null=True)
    user_status = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    reg_by = models.IntegerField(blank=True, null=True)
    m_date = models.DateTimeField(blank=True, null=True)
    m_by = models.IntegerField(blank=True, null=True)
    failure_attempts = models.IntegerField(blank=True, null=True)
    secretanswer = models.CharField(max_length=225, blank=True, null=True)
    ipaddress = models.CharField(max_length=225, blank=True, null=True)
    macaddress = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.firstname + " " + self.email)

    class Meta:
        managed = False
        db_table = 'users'


class Week(models.Model):
    week_id = models.AutoField(primary_key=True)
    week = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.week)

    class Meta:
        managed = False
        db_table = 'week'


class Wellnessplan(models.Model):
    wellnessplan_id = models.AutoField(primary_key=True)
    wellnessplan_socialhistory = models.ForeignKey('WellnessplanSocialhistory', models.DO_NOTHING)
    wellnessplan_profession = models.ForeignKey('WellnessplanProfession', models.DO_NOTHING)
    conditions = models.ForeignKey(Conditions, models.DO_NOTHING)
    agegroup = models.ForeignKey(Agegroup, models.DO_NOTHING)
    medicalhistory = models.CharField(max_length=225, blank=True, null=True)
    surgicalhistory = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.medicalhistory)

    class Meta:
        managed = False
        db_table = 'wellnessplan'


class WellnessplanProfession(models.Model):
    wellnessplan_profession_id = models.AutoField(primary_key=True)
    wellnessplan_profession = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.wellnessplan_profession)

    class Meta:
        managed = False
        db_table = 'wellnessplan_profession'


class WellnessplanSocialhistory(models.Model):
    wellnessplan_socialhistory_id = models.AutoField(primary_key=True)
    wellnessplan_socialhistory = models.CharField(max_length=225, blank=True, null=True)
    sort_by = models.IntegerField(blank=True, null=True)
    status_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.wellnessplan_socialhistory)

    class Meta:
        managed = False
        db_table = 'wellnessplan_socialhistory'
