# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
'''

	All the models for the database
	Every model has to have a default value if the field
	is set to NOT NULL and ForeignKeys should specify default behaviour

'''

import datetime
import hashlib
import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User as admin_user
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# functions for default
def current_timestamp():
    return datetime.datetime.now()


'''
		COMMON MODELS INDEPENDENT OF
		SITE/ROLE SPECIFICS
'''


# Address and Location related models

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(unique=True, max_length=5)

    def __str__(self):
        return "<Country %s: %s >" % (self.code, self.name)

    class Meta:
        managed = True
        db_table = 'countries'


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=5)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "<State %s | %s: %s>" % (self.code, self.country.code, self.name)

    class Meta:
        managed = True
        db_table = 'states'


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=5)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "<City %s | %s | %s >" % (self.code, self.state.name, self.name)

    class Meta:
        managed = True
        db_table = 'cities'


# class District(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	name = models.CharField(max_length=60)
# 	code = models.CharField(max_length=5)
# 	city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

# 	class Meta:
# 		managed = True
# 		db_table = 'districts'

class Address(models.Model):
    ''' address, can be of the user or any other model
	'''
    location_type_options = (
        ('current', "Current Location"),
        ('manual', "Update Manually"),
    )
    resident_type_options = (
        ('home', "Home"),
        ('office', "Office"),
        ('other', "Other"),
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE, blank=True, null=True)
    location_type = models.CharField(choices=location_type_options, max_length=200, default='current')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, blank=True, null=True)
    door_no= models.CharField(max_length=200, blank=True, null=True)
    area= models.CharField(max_length=200, blank=True, null=True)
    landmark= models.CharField(max_length=200, blank=True, null=True)
    resident_type = models.CharField(choices=resident_type_options, max_length=200, default='home')
    pincode = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'address'


# Functionality models


class Coupon(models.Model):
    ''' coupons that can be used for discount
		across the board by anyone.
		these are made by the admin (phealth)
	'''
    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    type_choices = (
        ('percentage', '%'),
        ('amount', 'Rs'),
    )
    name = models.CharField(max_length=30)
    quantity = models.PositiveSmallIntegerField()
    validity = models.BooleanField(default=True)
    expiry = models.DateField()
    amount = models.PositiveSmallIntegerField(default=0)
    type = models.CharField(choices=type_choices, max_length=30, default='amount')

    date_added = models.DateTimeField(default=current_timestamp, editable=False)

    def __str__(self):
        return "<Coupon %s | Q : %d | %d %s >" % (self.name, self.quantity, self.amount, self.type)

    class Meta:
        managed = True
        db_table = 'coupons'


# healthchecks and associated

class TestCategory(models.Model):
    ''' cateogeries for a given test
	'''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()

    class Meta:
        managed = True
        db_table = 'test_categories'


class TestSubcategory(models.Model):
    ''' subcategories for a given test
	'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = models.ForeignKey(TestCategory, on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'test_subcategories'


class Test(models.Model):
    ''' the various tests offered by
		a healthprovider
	'''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)
    department = models.CharField(max_length=70)
    description = models.TextField()
    subcategory = models.ForeignKey(TestSubcategory, on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'tests'

class HealthCheckup(models.Model):
	''' Type of health checkup
		Sold by admins to sales agents ONLY
	'''
	applicability_options = (
		('0', "General"),
		('1', "Group/ Sponsored"),
	)

	id = models.AutoField(primary_key=True)
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=40, unique=True)
	description = models.TextField()
	price = models.PositiveSmallIntegerField(default=0)
	image = models.ImageField(upload_to='health_checks', default='default_healthcheck.jpg')
	tests = models.ManyToManyField(Test)
	applicability = models.CharField(choices=applicability_options, max_length=1, default=0)
	group_or_sponsor = models.ManyToManyField('User', null=True, blank=True)
	coupon= models.ManyToManyField('Coupon', null=True, blank=True)

	class Meta:
		managed = True
		db_table = 'healthchecks'


class DiscountCard(models.Model):
	''' discount card sold by sponsors
	and sales agents for use in combo healthchecks
	These cards are sold
	'''
	restriction_options = (
		('0', "No"),
		('1', "Yes"),
	)
	applicability_options = (
		('0', "General"),
		('1', "Group/ Sponsored"),
	)

	id = models.AutoField(primary_key=True)
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	code = models.CharField(max_length=3)
	name = models.CharField(max_length=40, unique=True)
	image = models.ImageField(upload_to='discountcard', default='default_discountcatd.jpg')
	description = models.TextField(null=True, blank=True)
	quantity = models.PositiveSmallIntegerField(default=0)
	coverage = models.PositiveSmallIntegerField(default=0)
	restriction = models.CharField(choices=restriction_options, max_length=1, default=0)
	applicable_family_members= models.ManyToManyField('Familymember', null=True, blank=True)
	applicability = models.CharField(choices=applicability_options, max_length=1, default=0)
	group_or_sponsor = models.ManyToManyField('User', null=True, blank=True)
	price = models.PositiveSmallIntegerField(default=0)
	price_extra_member = models.PositiveSmallIntegerField(default=0)
	extra_family_members= models.ManyToManyField('Familymember', null=True, blank=True,related_name='extra_family_members')
	validity = models.DateField()

	health_checkups = models.ManyToManyField(HealthCheckup)
	coupon= models.ManyToManyField('Coupon', null=True, blank=True)

	class Meta:
		managed = True
		db_table = 'discountcards'



class Speciality(models.Model):
    ''' hospital/clinician specialities
	'''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return "<Speciality: %s | %s... >" % (self.name, self.description[:15])

    class Meta:
        managed = True
        db_table = 'specialities'


# user associated

class Question(models.Model):
    ''' question used for recovery etc
	'''
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=100)

    def __str__(self):
        return "<Question: %s >" % self.question

    class Meta:
        managed = True
        db_table = 'questions'


class User(models.Model):
    ''' Main user object who will consist of all information
	'''

    id = models.AutoField(primary_key=True)
    role_choices = (
        # primary roles
		('healthprovider', 'healthprovider'),  # hospital
		('healthseeker', 'healthseeker'),  # actual user
		('clinician', 'clinician'),  # actual doctor
		('sponsor', 'sponsor'),  # group user setting

		# secondary roles
		('poc', 'poc'),  # sponsor poc
		('salesagent', 'salesagent'),  # sells plans from admin
		('reseller', 'reseller'),  # buys healthcards from agents

		# admin based roles and misc
		('editor', 'editor'),  # editor for a given blog
		('admin', 'admin'),  # main admin dashboard

    )

    basic_education_choices = (

        ('10', '10'),
        ('10+2', '10+2'),

    )

    post_graduate_choices = (
        ('none', 'none'),
        ('pg', 'pg'),
        ('pglist', 'pglist'),
    )

    diploma_choices = (
        ('none', 'none'),
        ('diploma', 'diploma'),
        ('diplomalist', 'diplomalist'),
    )

    super_speciality_choices = (
        ('none', 'none'),
        ('super_speciality1', 'super_speciality1'),
        ('super_speciality2', 'super_speciality2'),
    )
    # whether the user is active or not
    status = models.NullBooleanField(default=True, editable=False)
    role = models.CharField(choices=role_choices, editable=False, max_length=30)
    reg_date = models.DateTimeField(default=current_timestamp, editable=False)
    last_update = models.DateTimeField(editable=False)
    last_IP = models.GenericIPAddressField(editable=False, default='127.0.0.1')

    email = models.EmailField()
    name = models.CharField(max_length=150)
    mobile = models.CharField(validators=[
        RegexValidator(
            regex=r'^(\+\d{1,3}[- ]?)?\d{10}$',
            message="Invalid Number")], max_length=15)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),), default="F")

    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, default=1)
    answer = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics',
                                    default='default_profile.jpg')

    # NEW FIELDS ADDED FOR EDUCATION OF USER
    basic_education = models.CharField(choices=basic_education_choices, max_length=30, default='10')
    post_graduate = models.CharField(choices=post_graduate_choices, max_length=30, default='none')
    diploma = models.CharField(choices=diploma_choices, max_length=30, default='none')
    super_speciality = models.CharField(choices=super_speciality_choices, max_length=30, default='none')
    other_trainings = models.TextField(default="TEST")
    other_degrees = models.TextField(default="TEST1")
    dob = models.DateField(default=current_timestamp)

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        self.last_update = datetime.datetime.now()
        super(User, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'users'


class Transaction(models.Model):
    ''' any sort of payment transaction
	'''
    status_options = (
        ('1', "Paid to Pheatlh"),
        ('2', "Paid to user"),
        ('3', "Pending"),
        ('4', "Failed"),
    )
    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    IP = models.GenericIPAddressField(editable=False)
    timestamp = models.DateTimeField(default=
                                     current_timestamp, editable=False)

    sender = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='issued')
    receiver = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='received', null=True, blank=True)
    amount = models.PositiveSmallIntegerField(default=0)

    status = models.CharField(choices=status_options, max_length=1)

    class Meta:
        managed = True
        db_table = 'transactions'


'''
		SPECIFIC ROLE BASED MODELS

'''


class Seeker(models.Model):
    ''' the common user who will be using the platform
	'''

    profession_choices = (
        ('doctor', 'doctor'),
        ('teacher', 'teacher'),
        ('engineer', 'engineer'),
        ('professor', 'professor'),
        ('business', 'business'),
        ('other', 'other'),
    )


    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    family = models.ForeignKey(User,related_name='family', on_delete=models.DO_NOTHING, null=True, blank=True)
    appointments = models.ManyToManyField('Appointment', editable=False)
    profession = models.CharField(max_length=100, choices=profession_choices, default="other")
    language = models.ManyToManyField('Languages',  null=True, blank=True)


    healthchecks = models.ManyToManyField(HealthCheckup, null=True, blank=True)

    def __str__(self):
        return "<Seeker : %s >" % self.user.email

    class Meta:
        managed = True
        db_table = 'seekers'


class Clinician(models.Model):
    ''' the doctor who belongs to a given Provider
	'''
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    specialities = models.ManyToManyField(Speciality)

    # [ [start_time, end_time], ... <7 days> ]
    work_timings = ArrayField(
        ArrayField(
            models.TimeField(),
            size=2),
        size=7, null=True, blank=True)

    # [ [start_time, end_time], ... <7 days> ]
    break_timings = ArrayField(
        ArrayField(
            models.TimeField(),
            size=2),
        size=7, null=True, blank=True)

    # [ [start_date, end_date], ... ]
    vacations = ArrayField(
        ArrayField(
            models.DateField(),
            size=2), null=True, blank=True, default=[])

    def check_availability(self, from_date, to_date):
        ''' given from and to, check whether the clinician
			is available for the given period.
			@param from_date -> datetime.date
			@param to_date -> datetime.date
			@return boolean
		'''
        try:
            if not isinstance(from_date, datetime.date):
                from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
            if not isinstance(to_date, datetime.date):
                to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        except:
            return False

        if to_date < from_date: return False
        for date_slot in self.vacations:
            start_date, end_date = date_slot
            if from_date >= start_date and to_date <= end_date:
                return False
        return True

    def check_session(self, session):
        '''
			given a session, check if a doctor is available in that session
			@param session -> str "morning"/"afternoon"/"evening"
			@return True/False
		'''
        get_time = lambda x: datetime.datetime.strptime(x, '%H:%M').time()
        session_timings = {
            'morning': get_time('11:00'),
            'afternoon': get_time('16:00'),
            'evening': get_time('21:00'),
            'night': get_time('23:59'),
        }

        if session not in session_timings: return False
        for time_slot in self.work_timings:
            if time_slot[0] <= session_timings[session] <= time_slot[1]:
                return True
        return False

    education = models.TextField()
    experience = ArrayField(models.TextField(), null=True, blank=True)

    ##NEW ROUTES ADDED
    offerings = ArrayField(models.TextField(), null=True, blank=True)
    conditions_treated = ArrayField(models.TextField(), null=True, blank=True)
    procedures = ArrayField(models.TextField(), null=True, blank=True)
    awards = ArrayField(models.TextField(), null=True, blank=True)
    fee = models.PositiveSmallIntegerField(default=0)
    amount = models.PositiveSmallIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(default=0)
    discount_sub = models.PositiveSmallIntegerField(default=0)
    registrations = ArrayField(models.TextField(), null=True, blank=True)
    memberships = ArrayField(models.TextField(), null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'clinicians'


class Provider(models.Model):
    ''' the hospital that may or may not be a branch
	'''

    type_choices = (
        ('clinic', 'clinic'),
        ('hospital', 'hospital'),
        ('diagnostic_centre', 'diagnostic center'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="Generic Hospital")
    type = models.CharField(choices=type_choices, default='hospital', max_length=30)
    active_from = models.DateField(default=current_timestamp)

    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    poc = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    is_branch = models.BooleanField(default=False)
    parent_provider = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True)

    clinicians = models.ManyToManyField(Clinician)
    specialities = models.ManyToManyField(Speciality)
    ## New Fields added
    facilities = ArrayField(models.TextField(), null=True, blank=True)
    offerings = ArrayField(models.TextField(), null=True, blank=True)
    special_checks = ArrayField(models.TextField(), null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'providers'


class Organization(models.Model):
    '''
		comprises the org of a given sponsor
	'''

    org_type_choices = (
        ("corporate", "Corporations"),
        ("college", "Educational Institutions"),
        ("ngo", "Non-government Organizations"),
        ("community", "Gated communities"),
    )

    org_size_choices = (
        ("50-100", "50-100"),
        ("100-500", "100-500"),
        ("500-1000", "500-1000"),
        ("1000-5000", "1000-5000"),
        ("5000-10000", "5000-10000"),
        ("10000+", "10000+"),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    size = models.CharField(choices=org_size_choices, max_length=30, default="50-100")
    type = models.CharField(choices=org_type_choices, max_length=100, default="corporate")
    location = models.OneToOneField(Address, on_delete=models.DO_NOTHING, null=True, blank=True)


class Sponsor(models.Model):
    ''' the sponsor who can bulk register users as seekers
	'''

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='poc')
    organization = models.OneToOneField(Organization, on_delete=models.DO_NOTHING)
    pocs = models.ManyToManyField(User, blank=True, null=True, related_name='pocs')
    users = models.ManyToManyField(Seeker, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sponsors'


class Reseller(models.Model):
    ''' the person who buys discount cards from the SalesAgent
	'''
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    discount_cards = HStoreField(null=True, blank=True, editable=False)

    class Meta:
        managed = True
        db_table = 'resellers'


class SalesAgent(models.Model):
    ''' the person who buys discount cards from the admin
	'''
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    discount_cards = HStoreField(null=True, blank=True, editable=False)
    resellers = models.ManyToManyField(Reseller)

    class Meta:
        managed = True
        db_table = 'salesagents'


'''

	role specific models

'''


class Appointment(models.Model):
    ''' appointments made by the user
	'''
    status_options = (
        ('pending', 'pending'),
        ('confirmed', 'confirmed'),
        ('cancelled', 'cancelled'),
        ('rescheduled', 'rescheduled'),
    )

    CSS_options = (
        ('event-info', 'Info'),
        ('event-success', 'Success'),
        ('event-warning', 'Warning'),
        ('event-special', 'Special'),
    )

    # indexing and meta fields
    id = models.AutoField(primary_key=True)
    create_on = models.DateTimeField(default=current_timestamp, editable=False)
    date_modified = models.DateTimeField(default=current_timestamp, editable=False)

    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(default=30)
    status = models.CharField(choices=status_options, default='pending', max_length=40)
    under = models.ForeignKey(Clinician, on_delete=models.DO_NOTHING, null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING, null=True, blank=True)

    # calendar config fields
    from_timestamp = models.DateTimeField(default=current_timestamp, editable=False)
    to_timestamp = models.DateTimeField(default=current_timestamp, editable=False)
    css_class = models.CharField(max_length=20, choices=CSS_options, editable=False, default='event-info')

    def __str__(self):
        return "<A: %s -> %s >" % (self.date, self.time)

    def save(self, *args, **kwargs):
        self.date_modified = current_timestamp()

        self.from_timestamp = datetime.datetime.combine(self.date, self.time)
        self.to_timestamp = self.from_timestamp + datetime.timedelta(minutes=self.duration)

        ops, css = [_[0] for _ in self.status_options], [_[0] for _ in self.CSS_options]
        self.css_class = css[ops.index(self.status)]

        super(Appointment, self).save(*args, **kwargs)


class Testimonial(models.Model):
    ''' user testimonials
	'''
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    user = models.OneToOneField(Seeker, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(default=current_timestamp)

    class Meta:
        managed = True
        db_table = 'testimonials'


class CDN(models.Model):
    ''' static content across the site will
		be maintained by this table
	'''
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='cdn', blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    code = models.CharField(max_length=30, default='misc')
    description = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(default=current_timestamp, editable=False)
    date_modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.date_modified = current_timestamp()
        super(CDN, self).save(*args, **kwargs)

    def __str__(self):
        return "<Content %s | %s >" % (self.image, self.description)

    class Meta:
        managed = True
        db_table = 'images'


# blog posts

class BlogCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=30)

    featured_posts = models.ManyToManyField('Post', null=True, blank=True)

    def __str__(self):
        return "<Category: %s>" % (self.name)

    class Meta:
        managed = True
        db_table = 'blog_categories'


class Post(models.Model):
    '''
		blog posts will be of this type
	'''
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='blog', default='default_blog.jpg')
    url = models.URLField(null=True, blank=True)
    clicks = models.PositiveSmallIntegerField(default=0, editable=False)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    comment_count = models.PositiveSmallIntegerField(default=0, editable=False)
    category = models.ForeignKey(BlogCategory, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(default=current_timestamp, editable=False)
    date_modified = models.DateTimeField(editable=False)

    def __str__(self):
        return "<Post : %s | %s >" % (self.uid, self.title)

    def save(self, *args, **kwargs):
        self.date_modified = current_timestamp()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'posts'


class BlogComment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    date_added = models.DateTimeField(default=current_timestamp, editable=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, editable=False)

    def save(self, *args, **kwargs):
        self.post.comment_count += 1
        self.post.save()
        super(BlogComment, self).save(*args, **kwargs)

    def __str__(self):
        return "<Comment %s | %s >" % (self.user.email, self.text[:20] + "...")

    class Meta:
        managed = True
        db_table = 'blog_comments'


class Symptoms(models.Model):
    symptomarea = models.ForeignKey('SymptomsArea', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class SymptomsArea(models.Model):
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Facility(models.Model):
    facility_type = models.ForeignKey('FacilityType', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class FacilityType(models.Model):
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Timesession(models.Model):
    name = models.CharField(max_length=200)
    fromtime = models.TimeField(null=True, blank=True)
    totime = models.TimeField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=200)
    subrole = models.CharField(max_length=200,null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Familymember(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name


class Languages(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

class IdConfiguration(models.Model):
    affix = models.CharField(max_length=200,null=True, blank=True)
    prefix = models.CharField(max_length=200,null=True, blank=True)
    tablename = models.CharField(max_length=200,null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.affix


class HealthProviderPlans(models.Model):
	''' Type of health checkup
		Sold by admins to sales agents ONLY
	'''
	validity_options = (
		('6', "6 Months"),
		('12', "12 Months"),
		('24', "24 Months"),
		('36', "36 Months"),
	)
	licence_options = (
		('12', "12 Months"),
		('24', "24 Months"),
		('36', "36 Months"),
	)
	applicability_options = (
		('0', "General"),
		('1', "Specific Service Provider"),
	)
	name = models.CharField(max_length=200)
	price = models.PositiveSmallIntegerField(default=0)
	amount_credit = models.PositiveSmallIntegerField(default=0)
	image = models.ImageField(upload_to='plans', default='default_healthprovider_plan.jpg')
	description = models.TextField()
	first_consultation_share = models.PositiveSmallIntegerField(default=0)
	subsequent_consultation_share = models.PositiveSmallIntegerField(default=0)
	first_consultation_discount = models.PositiveSmallIntegerField(default=0)
	subsequent_consultation_discount = models.PositiveSmallIntegerField(default=0)
	validity = models.CharField(choices=validity_options, max_length=200, default=0)
	speciality_group = models.ManyToManyField(Group)
	software_licence = models.CharField(choices=licence_options, max_length=200, default=0)
	applicability = models.CharField(choices=licence_options, max_length=200, default=0)
	service_provider = models.ManyToManyField('User', null=True, blank=True)
	coupon= models.ManyToManyField('Provider', null=True, blank=True)

	def __str__(self):
		return self.name