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
import math
import uuid
from decimal import Decimal

from django.contrib.auth.models import User as admin_user
from django.contrib.postgres.fields import (ArrayField, HStoreField,
                                            IntegerRangeField, JSONField, DateRangeField)
from django.contrib.postgres.fields.jsonb import JSONField as JSONBField
from django.contrib.postgres.validators import KeysValidator, ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# functions for default
def current_timestamp():
	return datetime.datetime.now()


class Location(models.Model):

	id = models.AutoField(primary_key=True)
	place_id = models.CharField(max_length=128, unique=True, editable=False) # used to reference the place using maps API
	name = models.CharField(max_length=100) # can be used for object referral
	full_name = models.CharField(max_length=200) # can be used to display
	extra = models.CharField(max_length=50, null=True, blank=True) # can be used to store door no, and other info

	lat = models.DecimalField(max_digits=8, decimal_places=5)
	long = models.DecimalField(max_digits=8, decimal_places=5)

	rad_lat = models.DecimalField(max_digits=8, decimal_places=5, editable=False) # internal field for calculation
	rad_long = models.DecimalField(max_digits=8, decimal_places=5, editable=False) # internal field for calculation

	landmark = models.CharField(max_length=100) # used for lazy grouping

	# direct storage of address components
	# this field adapts directly from the JSON returned by the MAPS API
	# type -> Array | len -> 7 | assert(eles == JSON) |
	# keys -> long_name <String>, short_name <String>, types <Array>
	address_component = JSONBField(JSONField(validators=[
	]), default=(7 * [{'long_name' : "", 'short_name' : "", 'types' : [] }]), editable=False)

	class Meta:
		managed = True
		db_table = 'locations'


	def __init__(self, *args, **kwargs):
		'''
			@description override init to directly init the values from the google place API
			accepts a JSON as follows:
			place = {
				'place_id' : <String>,
				'name' : <String>,
				'formatted_address' : <String>,
				'vicinity' : <String>, // corresponds to landmark

				'location' : {
					'lat' : <Decimal 8,5>,
					'lng' : <Decimal 8,5>,
				},

				'address_component' : [
					{
						'short_name' : <String>,
						'long_name' : <String>,
						'types' : <Array>,
					}, ... <7 records>
				],
			}
			@param [place] -> JSON
			@params (opt.) keys
		'''
		place = kwargs.pop('place', None)
		super(Location, self).__init__(*args, **kwargs)
		if place is not None:
			self.place_id = place['place_id']
			self.full_name = place['formatted_address']
			try:
				self.name = place['name']
			except KeyError:
				self.name = ', '.join(self.full_name.split(',')[:3])

			self.lat = Decimal(str(round(float(place['location']['lat']), 5)))
			self.long = Decimal(str(round(float(place['location']['lng']), 5)))
			try:
				self.landmark = place['vicinity']
			except KeyError:
				self.landmark = self.name
			self.address_component = place['address_components']


	def __str__(self):
		''' pretty repr for an instance '''
		return "%s | %f, %f" % (self.full_name, self.lat, self.long)


	def clean(self, *args, **kwargs):
		''' override to check validity of address_components '''

		# address_component checking
		error_msg = "Invalid address_component | %s"
		# length check
		if len(self.address_component) < 1:
			raise ValidationError({ 'address_component' : error_msg % "Length is invalid" })
		# JSON sanity check
		if not all([isinstance(_, dict) for _ in self.address_component]):
			raise ValidationError({ 'address_component' : error_msg % "Components are not all JSON" })
		# key validation
		if not all([all([_ in ['short_name', 'long_name', 'types'] for _ in x])
			for x in self.address_component]):
			raise ValidationError({ 'address_component' : error_msg % "Invalid keys" })
		# key type validation
		if not all(all([isinstance(_['short_name'], str), isinstance(_['long_name'], str),
			 isinstance(_['types'], list), ]) for _ in self.address_component):
			raise ValidationError({ 'address_component' : error_msg % "Invalid key type(s)" })

		return super().clean(*args, **kwargs)


	def save(self):
		''' override save to save internal fields at model level '''
		self.full_clean()
		self.rad_lat = math.radians(self.lat)
		self.rad_long = math.radians(self.long)
		super().save()


	def getCoords(self):
		''' returns the lat, long of the current location '''
		return { 'lat' : self.lat, 'long' : self.long }


	def getDistance(self, lat, lng):
		'''
			@description returns the distance between a given place and this current location

			if
				φ1 = lat1.toRadians()
				φ2 = lat2.toRadians()
				Δλ = (lon2-lon1).toRadians()
				R = 6371e3;
			then
				return acos( Math.sin(φ1) * Math.sin(φ2) + Math.cos(φ1) * Math.cos(φ2) * Math.cos(Δλ) ) * R

			@param lat -> decimal field
			@param lng -> decimal field
			@return dist -> float, metres
		'''
		distance = 0
		rad_lat_2 = math.radians(lat)
		del_lng = math.radians(lng - self.long)
		R = 6371e3
		distance = math.acos( math.sin(self.rad_lat) * math.sin(rad_lat_2) + \
			math.cos(self.rad_lat) * math.cos(rad_lat_2) * math.cos(del_lng) ) * R
		return distance


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


class Test(models.Model):
	''' the various tests offered by
		a healthprovider
	'''

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=40)
	code = models.CharField(max_length=10)
	department = models.CharField(max_length=70)
	description = models.TextField()
	# subcategory = models.ForeignKey(TestSubcategory, on_delete=models.DO_NOTHING)
	test_image = models.ImageField(upload_to='test_pic', blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'tests'

	def __str__(self):
		return self.name


class TestCategory(models.Model):
	''' cateogeries for a given test
	'''

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=40)
	description = models.TextField()
	category_pic = models.ImageField(upload_to = 'test_categories', null=True, blank=True)
	test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE)

	class Meta:
		managed = True
		db_table = 'test_categories'

	def __str__(self):
		return self.name


class TestSubcategory(models.Model):
	''' subcategories for a given test
	'''
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=40)
	description = models.TextField()
	category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, blank=True, null=True)
	sub_category_image = models.ImageField(upload_to='sub_catagory_pic', blank=True, null=True)


	class Meta:
		managed = True
		db_table = 'test_subcategories'

	def __str__(self):
		return self.name




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


class Amenity(models.Model):
	'''
	Hospital provides the following amenities for its patients and visitors:
	'''
	service_name = models.CharField(max_length=40)
	service_image = models.ImageField(upload_to='amenities', null=True, blank=True)

	def __str__(self):
		return self.service_name


class HealthCheckup(models.Model):
	''' Type of health checkup
		Sold by admins to sales agents ONLY
	'''

	applicability_options = (
		('0', "General"),
		('1', "Group/ Sponsored"),
	)

	type_choices = (
		('preventive', 'preventive'),
		('diabetes', 'diabetes'),
		('cancer', 'cancer'),
		('antenatal', 'antenatal'),
		('other', 'other'),
	)

	gender_choices = (
		('male', 'male'),
		('female', 'female'),
		('both', 'both'),
	)

	id = models.AutoField(primary_key=True)
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=40, unique=True)
	type = models.CharField(max_length=35, choices=type_choices, default='preventive')

	gender = models.CharField(default='both', choices=gender_choices, max_length=5)

	# querying the field can be done with the following
	# from psycopg2.extras import NumericRange
	# HealthCheckup.objects.filter(age__contained_by=NumericRange(0, 40))
	age = IntegerRangeField()
	pre_existing_conditions = models.ForeignKey(Speciality, on_delete=models.CASCADE, 
		null=True, blank=True)

	tests = models.ManyToManyField(Test)
	description = models.TextField()
	price = models.PositiveSmallIntegerField(default=0)
	image = models.ImageField(upload_to='health_checks', default='default_healthcheck.jpg')

	applicability = models.CharField(choices=applicability_options, max_length=1, default=0)

	group_or_sponsor = models.ManyToManyField('User', null=True, blank=True)
	coupon= models.ManyToManyField('Coupon', null=True, blank=True)
	instructions = models.TextField(null=True, blank=True)


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


	# whether the user is active or not
	status = models.NullBooleanField(default=True, editable=False)
	role = models.CharField(choices=role_choices, editable=False, max_length=30)
	reg_date = models.DateTimeField(default=current_timestamp, editable=False)
	last_update = models.DateTimeField(editable=False)
	last_IP = models.GenericIPAddressField(editable=False, default='127.0.0.1')

	email = models.EmailField()
	name = models.CharField(max_length=150)
	dob = models.DateField(default=current_timestamp)
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

	location = models.ForeignKey(Location, on_delete=models.DO_NOTHING,null=True, blank=True)
	relation = models.ForeignKey('Familymember', on_delete=models.DO_NOTHING,null=True, blank=True)

	dob = models.DateField(default=current_timestamp)
	profession = models.CharField(max_length=100, choices=profession_choices, default="other")
	language = models.CharField(max_length=100, choices=language_choices, default="english")

	family = models.OneToOneField(User,related_name='family', on_delete=models.DO_NOTHING, null=True, blank=True)

	appointments = models.ManyToManyField('Appointment', editable=False)
	healthchecks = models.ManyToManyField(HealthCheckup, null=True, blank=True)
	transactions = models.ManyToManyField(Transaction, null=True, blank=True, editable=False)

	def __str__(self):
		return "<Seeker : %s >" % self.user.email

	class Meta:
		managed = True
		db_table = 'seekers'


class Clinician(models.Model):
	''' the doctor who belongs to a given Provider
	'''

	language_choices = (
		('hindi', 'Hindi'),
		('english', 'English'),
		('bengali', 'Bengali'),
		('telugu', 'Telugu'),
		('marathi', 'Marathi'),
		('tamil', 'Tamil'),
		('urdu', 'Urdu'),
		('kannada', 'Kannada'),
		('gujarati', 'Gujarati'),
		('bhojpuri', 'Bhojpuri'),
		('odia', 'Odia'),
		('malayalam', 'Malayalam'),
		('sanskri', 'Sanskri'),
		('other', 'other'),
	)

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	specialities = models.ManyToManyField(Speciality)
	language = models.CharField(max_length=100, choices=language_choices, default="other")

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

	def get_def_discount():
		'''
			@description default discounts available
			@return list
		'''
		discounts = []
		services = ['Out Patient Services', 'Emergency Room',
		 'Day Care Procedures', 'Lab Services', 'Speciality']
		for service in services:
			discounts.append({
				'name' : service,
				'type' : 'offering',
				'amount' : 0,
				'description' : "",
			})
		fees = ['First time', 'Subsequent fees']
		for fee in fees:
			discounts.append({
				'name' : fee,
				'type' : "fee",
				'amount' : 0,
				'description' : ""
			})
		return discounts

	# JSON-based and other account related fields

	# fees -> correlate with discount_offerings
	first_fee = models.PositiveSmallIntegerField(default=0)
	fee = models.PositiveSmallIntegerField(default=0)

	# education locations and other details can be stored here
	education = JSONBField(JSONField(validators=[
	KeysValidator(['year', 'title', 'description', 'type'])
	]), null=True, blank=True, default=list)

	# experience/training obtained in an institute
	experience_training = JSONBField(JSONField(validators=[
		KeysValidator(['year', 'position', 'description', 'type'])
	]), null=True, blank=True, default=list)

	# various types of discounts and offerings offered
	discount_offerings = JSONBField(JSONField(validators=[
		KeysValidator(['name', 'amount', 'type', 'description'])
	]), default=get_def_discount)

	# procedure or conditions storage
	procedure_conditions = JSONBField(JSONField(validators=[
		KeysValidator(['name', 'description', 'type', 'date'])
	]), null=True, blank=True, default=list)

	# awards and recognition
	awards = JSONBField(JSONField(validators=[
		KeysValidator(['name', 'description', 'year', 'recognised_by'])
	]), null=True, blank=True, default=list)

	# registrations
	registrations = JSONBField(JSONField(validators=[
		KeysValidator(['name', 'reg_no', 'year',])
	]), null=True, blank=True, default=list)

	# memberships
	memberships = JSONBField(JSONField(validators=[
		KeysValidator(['name', 'country', 'city',])
	]), null=True, blank=True, default=list)

	def clean(self):
		'''
			override the clean function for JSON validation
		'''
		validators = [
			('education', KeysValidator(['year', 'title', 'description', 'type',])),
			('experience_training', KeysValidator(['year', 'position', 'description', 'type',])),
			('discount_offerings', KeysValidator(['name', 'amount', 'type', 'description',])),
			('procedure_conditions', KeysValidator(['name', 'description', 'type', 'date',])),
			('awards', KeysValidator(['name', 'description', 'year', 'recognised_by',])),
			('registrations', KeysValidator(['name', 'reg_no', 'year',])),
			('memberships', KeysValidator(['name', 'country', 'city',])),
		]
		errors = []
		cleaned_fields = super().clean()
		for field, validator in validators:
			for record in cleaned_fields[field]:
				print(record)
				try:
					_ = validator(record)
				except ValidationError as e:
					errors.append(e)
		if len(errors):
			raise ValidationError(errors)
		return cleaned_fields


	def save(self, *args, **kwargs):
		''' save override to call validation '''
		#self.full_clean()
		super().save(*args, **kwargs)


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

	class Meta:
		managed = True
		db_table = 'clinicians'



class BasicFaciltyModel(models.Model):
	'''
	Common model for facilities provided by Hospital
	'''
	name = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)

	class Meta:
		abstract = True


class Diagnostic(BasicFaciltyModel):
	'''
	diagnostics provided by hospital
	'''
	image = models.ImageField(upload_to='diagnostic_pics', blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		managed = True
		db_table = 'diagnostics'



class InsuranceCorporateRecognation(BasicFaciltyModel):
	'''
	Insurance or Corporate Recognations provided by hospital
	'''
	image = models.ImageField(upload_to='insurance_pics', blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		managed = True
		db_table = 'insurances'


class QualityAccreditation(BasicFaciltyModel):
	'''
	QualityAccreditation provided by hospital
	'''
	image = models.ImageField(upload_to='quality_pics', blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		managed = True
		db_table = 'quality_accreditations'


class ServiceType(models.Model):
	name = models.CharField(max_length=200)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name


class FacilityType(models.Model):
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	created_date = models.DateTimeField(default=timezone.now)
	icon = models.ImageField(upload_to='facility_type', blank=True, null=True)

	def __str__(self):
		return self.name


class Facility(models.Model):
	facility_type = models.ForeignKey(FacilityType, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	created_date = models.DateTimeField(default=timezone.now)
	icon = models.ImageField(upload_to='facility', blank=True, null=True)


	def __str__(self):
		return self.name


class Provider(models.Model):
	''' the hospital that may or may not be a branch
	'''

	# type_choices = (
	# 	('clinic', 'clinic'),
	# 	('hospital', 'hospital'),
	# 	('diagnostic_centre', 'diagnostic center'),
	# )

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, default="Generic Hospital")
	# type = models.CharField(choices=type_choices, default='hospital', max_length=30)
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	active_from = models.DateField(default=current_timestamp)

	location = models.ForeignKey(Location, on_delete=models.DO_NOTHING,null=True, blank=True)
	poc = models.ForeignKey(User, on_delete=models.DO_NOTHING)

	is_branch = models.BooleanField(default=False)
	parent_provider = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True)

	clinicians = models.ManyToManyField(Clinician,null=True, blank=True)
	amenities = models.ManyToManyField(Amenity,null=True, blank=True)
	specialities = models.ManyToManyField(Speciality,null=True, blank=True)
	healthchecks = models.ManyToManyField(HealthCheckup, null=True, blank=True)

	facilities = models.ManyToManyField(FacilityType, null=True, blank=True)
	offerings = ArrayField(models.TextField(), null=True, blank=True)
	special_checks = ArrayField(models.TextField(), null=True, blank=True)

	work_timings = ArrayField(
		ArrayField(
			models.TimeField(),
			size=2),
		size=7, null=True, blank=True)
	
	fax = models.BigIntegerField(blank=True, null=True)
	contact_person = models.CharField(max_length=50, blank=True, null=True)
	contact_number = models.PositiveIntegerField(blank=True, null=True)
	no_of_beds = models.PositiveIntegerField(blank=True, null=True)


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

	def __str__(self):
		return self.name

	class Meta:
		managed = True
		db_table = 'providers'

class Feedback(models.Model):
	'''
		The feedback/complaint for a given provider AND/OR clinician
		- Ratings for the various parameters (optional)
		- User, provider => compulsory
		- Clinician => optional
		- Appointment => The linked appointment object (optional)
		- categories => Types of parameters (set according to field setter)
			- Doctor
			- Clinic & Aminities
			- Staff & Hospitality
			- Timelines
	'''
	id = models.AutoField(primary_key=True)
	uid = models.UUIDField(editable=False, default=uuid.uuid4)
	date_added = models.DateTimeField(default=current_timestamp)

	user = models.ForeignKey(Seeker, on_delete=models.DO_NOTHING)
	message = models.TextField(null=True, blank=True, max_length=255)

	provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING)
	clinician = models.ForeignKey(Clinician, on_delete=models.DO_NOTHING, blank=True, null=True)
	appointment = models.ForeignKey('Appointment', on_delete=models.DO_NOTHING, blank=True, null=True)

	cat_keys = KeysValidator(['doctor', 'clinic_amenities', 'staff_hospitality', 'scheduling'])

	def get_categories():
		''' set the default categories according to the ones being validated '''
		cats = {}
		[cats.update({_ : 0}) for _ in Feedback.cat_keys.keys]
		return cats

	categories = JSONField(validators=[cat_keys], default=get_categories)

	class Meta:
		managed = True
		db_table = 'feedbacks'


	def clean(self, *args, **kwargs):
		''' override to check validity of categories '''

		error_msg = "%s error | %s"
		if not all([_ in Feedback.cat_keys.keys for _ in self.categories]):
			raise ValidationError({ 'categories' : error_msg % ("Keys", "Invalid Keys")})
		if not all([(isinstance(self.categories[_], int) or isinstance(self.categories[_], float)) and self.categories[_] >= 0
			and self.categories[_] <= 5 for _ in self.categories]):
			raise ValidationError({ 'categories' : error_msg % ("Values", "Invalid ratings")})
		elif self.clinician not in self.provider.clinicians.all():
			raise ValidationError({ 'clinician' : error_msg % ("Clinician", "Clinician does not belong to provider!")})
		return super().clean(*args, **kwargs)


	def save(self):
		''' override save to save internal fields at model level '''
		self.full_clean()
		super().save()
		if self.appointment: self.appointment.save()


class Alert(models.Model):
	'''
		@description Notifier system to send alerts to patients
		@field uid => Unique identifier
		@field status => Internal field to trigger current active status
		@field name -> Desired Alert name
		@field type -> Type of alert
		@field method -> Means of alerting
		@field duration -> Range of dates to be alerted for
		@field contact -> Person to alert
	'''

	alert_choices = (
		('medication', 'medication'),
		('checkup', 'checkup'),
		('appointment', 'appointment'),
		('consultation', 'consultation'),
		('other', 'other'),
	)

	method_choices = (
		('email', 'email'),
		('mobile', 'mobile'),
		('both', 'both'),
		('none', 'none'),
	)

	id = models.AutoField(primary_key=True)
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	status = models.BooleanField(default=False, editable=False)

	name = models.CharField(max_length=30)
	type = models.CharField(max_length=40, choices=alert_choices, default='consultation')
	method = models.CharField(max_length=15, default='mobile', choices=method_choices)
	duration = DateRangeField()
	contact = models.ForeignKey(Seeker, on_delete=models.DO_NOTHING, editable=False)

	def __str__(self):
		return "%s (%s) | %s" % (self.name, self.type, self.status)


	def save(self, *args, **kwargs):
		dur = self.duration
		try:
			self.status = self.status or (dur[0] <= current_timestamp().date() <= dur[1])
		except TypeError:
			self.status = self.status or (dur.lower <= current_timestamp().date() <= dur.upper)

		super().save(*args, **kwargs)

	class Meta:
		db_table = 'alerts'
		managed = True


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
	image = models.ImageField(upload_to='organization_images', default='default_org.jpg')
	location = models.OneToOneField(Location, on_delete=models.DO_NOTHING, null=True, blank=True)


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


class Appointment(models.Model):
	''' appointments made by the user
	'''
	status_options = (
		('pending', 'pending'),
		('confirmed', 'confirmed'),
		('cancelled', 'cancelled'),
		('rescheduled', 'rescheduled'),
		('completed', 'completed'),
	)

	CSS_options = (
		('event-info', 'Info'),
		('event-success', 'Success'),
		('event-warning', 'Warning'),
		('event-special', 'Special'),
		('event-danger', 'Danger'),
	)

	# indexing and meta fields
	id = models.AutoField(primary_key=True)
	uid = models.UUIDField(default=uuid.uuid4, unique=True)
	create_on = models.DateTimeField(default=current_timestamp, editable=False)
	date_modified = models.DateTimeField(default=current_timestamp, editable=False)

	date = models.DateField()
	time = models.TimeField()
	duration = models.PositiveIntegerField(default=30)
	status = models.CharField(choices=status_options, default='pending', max_length=40)
	reviewed = models.BooleanField(default=False, editable=False)

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
		self.reviewed = bool(Feedback.objects.filter(appointment=self))
		self.from_timestamp = datetime.datetime.combine(self.date, self.time)
		self.to_timestamp = self.from_timestamp + datetime.timedelta(minutes=self.duration)

		ops, css = [_[0] for _ in self.status_options], [_[0] for _ in self.CSS_options]
		self.css_class = css[ops.index(self.status)]

		super(Appointment, self).save(*args, **kwargs)

	class Meta:
		db_table = 'appointments'
		managed = True
		unique_together = (('date', 'time', 'under', 'provider'),)


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
