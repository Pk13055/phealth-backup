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
		return "<State %s | %s: %s>" %(self.code, self.country.code, self.name)

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


class District(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=60)
	code = models.CharField(max_length=5)
	city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

	class Meta:
		managed = True
		db_table = 'districts'

class Address(models.Model):
	''' address, can be of the user or any other model
	'''
	id = models.AutoField(primary_key=True)
	district = models.ForeignKey(District, on_delete=models.DO_NOTHING)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	pincode = models.CharField(max_length=9)
	extra = models.CharField(max_length=100, blank=True, null=True)

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

	name = models.CharField(max_length=30)
	quantity = models.PositiveSmallIntegerField()
	validty = models.BooleanField(default=True)
	expiry = models.DateField()

	date_added = models.DateTimeField(default=current_timestamp, editable=False)

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
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=40, unique=True)
	description = models.TextField()
	price = models.PositiveSmallIntegerField(default=0)
	image = models.ImageField(upload_to='health_checks')
	tests = models.ManyToManyField(Test)

	class Meta:
		managed = True
		db_table = 'healthchecks'


class DiscountCard(models.Model):
	''' discount card sold by sponsors
	and sales agents for use in combo healthchecks
	These cards are sold
	'''
	id = models.AutoField(primary_key=True)
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	code = models.CharField(max_length=3)
	name = models.CharField(max_length=40, unique=True)
	description = models.TextField(null=True, blank=True)
	quantity = models.PositiveSmallIntegerField(default=0)
	price = models.PositiveSmallIntegerField(default=0)
	validity = models.DateField()

	health_checkups = models.ManyToManyField(HealthCheckup)

	class Meta:
		managed = True
		db_table = 'discountcards'

class Speciality(models.Model):
	''' hospital/clinician specialities
	'''

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()

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
		('healthprovider', 'healthprovider'), # hospital
		('healthseeker', 'healthseeker'), # actual user
		('clinician', 'clinician'), # actual doctor
		('sponsor', 'sponsor'), # group user setting
		# secondary roles
		('salesagent', 'salesagent'), # sells plans from admin
		('reseller', 'reseller'), # buys healthcards from agents

		# admin based roles and misc
		('editor', 'editor'), #editor for a given blog
		('admin', 'admin'), # main admin dashboard

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
		('O', 'Other'),))

	question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
	answer = models.CharField(max_length=100)
	profile_pic = models.ImageField(upload_to='profile_pics',
	 default='default_profile.jpg')

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
	receiver = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='received')
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

	language_choices = (
		('english', 'english'),
		('hindi', 'hindi'),
		('telugu', 'telugu'),
		('marathi', 'marathi'),
		('malayalam', 'malayalam'),
		('gujarati', 'gujarati'),
		('bhojpuri', 'bhojpuri'),
		('tamil', 'tamil'),
		('other', 'other'),
		)

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	family = models.ManyToManyField("self")
	appointments = models.ManyToManyField('Appointment', editable=False)
	profession = models.CharField(max_length=100, choices=profession_choices)
	language = models.CharField(max_length=100, choices=language_choices)
	dob = models.DateField()


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
			size=2), null=True, blank=True)

	education = models.TextField()
	experience = ArrayField(models.TextField(), null=True, blank=True)

	class Meta:
		managed = True
		db_table = 'clinicians'


class Provider(models.Model):
	''' the hospital that may or may not be a branch
	'''
	id = models.AutoField(primary_key=True)
	clinicians = models.ManyToManyField(Clinician)
	address = models.OneToOneField(Address, on_delete=models.DO_NOTHING)
	poc = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	parent_provider = models.OneToOneField("self", on_delete=models.DO_NOTHING, null=True, blank=True)
	is_branch = models.BooleanField(default=False)
	active_from = models.DateField()
	specialities = models.ManyToManyField(Speciality)

	class Meta:
		managed = True
		db_table = 'providers'


class Sponsor(models.Model):
	''' the sponsor who can bulk register users as seekers
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
	user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	org_name = models.CharField(max_length=50)
	org_size = models.CharField(choices=org_size_choices, max_length=30, default="50-100")
	org_type = models.CharField(choices=org_type_choices, max_length=100, default="corporate")
	users = models.ManyToManyField(Seeker, blank=True, null=True)
	# add extra fields after consulting

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
	id = models.AutoField(primary_key=True)
	create_on = models.DateTimeField(default=current_timestamp)
	date = models.DateField()
	time = models.TimeField()
	status = models.CharField(choices=status_options, default='pending', max_length=40)
	under = models.ForeignKey(Clinician, on_delete=models.DO_NOTHING, null=True, blank=True)
	provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING, null=True, blank=True)


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
