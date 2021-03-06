import datetime
import json
import random

import datatableview
import xlrd
from datatableview import Datatable
from datatableview.views import DatatableView, XEditableDatatableView
from django import forms
from django.contrib.auth.hashers import make_password
from django.core import serializers
from django.core.validators import RegexValidator
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views.generic.base import TemplateView
from querystring_parser import parser

from api.models import (DiscountCard, HealthCheckup, Location, Organization,
                        Question, Seeker, Sponsor, Transaction, User)
from common.views import send_OTP
from phealth.utils import get_sponsor, getIP, match_role, signin

# Create your views here.

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('__all__')
		widgets = {
			'password' : forms.PasswordInput()
		}


# sponsor common routes

def SignIn(request):
	''' basic route for the sponsor signin
	'''
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Sponsor Login",
			"route": "/sponsor",
			"color": "warning"
		})
	elif request.method == "POST":
		if signin(["sponsor", "poc"], request):
			return redirect('sponsor:dashboard_home')
		return redirect('sponsor:signin')


def SignUp(request):
	''' route for the signup of a new sponsor
	'''
	status = False
	class SponsorForm(forms.ModelForm):
		class Meta:
			model = User
			fields = ('email', 'name', 'mobile',
				'password', 'gender', 'question', 'answer')
			widgets = {
				'password' : forms.PasswordInput()
			}

	class OrganizationForm(forms.ModelForm):
		class Meta:
			model = Organization
			exclude = ('address',)

	class OTPForm(forms.Form):
		otp = forms.CharField(max_length=10)

		def __init__(self, *args, **kwargs):
			self.request = kwargs.pop('request', None)
			super().__init__(*args, **kwargs)

		def is_valid(self):
			init_validity = super().is_valid()
			if not init_validity: return False
			f = self.cleaned_data['otp']
			if str(f) != str(self.request.session['otp']):
				self.add_error('otp', "Invalid OTP")
				return False
			return True

	sponsor_form = SponsorForm()
	otp_form = OTPForm()
	if request.method == "POST":
		if "is_otp" in request.POST:
			status = True
			otp_form = OTPForm(request.POST, request=request)
			if otp_form.is_valid():
				del request.session['otp']
				return redirect('sponsor:signin')
			else:
				print(otp_form.errors)
		else:
			org_form = OrganizationForm(request.POST, request.FILES, prefix="org")
			sponsor_form = SponsorForm(request.POST, request.FILES)
			print(org_form.is_valid(), sponsor_form.is_valid())
			if org_form.is_valid() and sponsor_form.is_valid():
				organization = org_form.save()
				poc = sponsor_form.save(commit=False)
				poc.role = 'sponsor'
				poc.password = make_password(poc.password)
				poc.last_update = datetime.datetime.now()
				poc.save()
				sponsor = Sponsor(user=poc, organization=organization)
				sponsor.save()
				sponsor.pocs.add(poc)
				# request.POST['generate'] = True
				x = send_OTP(request, True)
				del x
				status = True
				print(request.session)
			else:
				print(org_form.errors, sponsor_form.errors)

	return render(request, 'sponsor/registration.html.j2', context={
		'title' : "Sponsor Registration",
		'sponsor_form' : sponsor_form,
		'otp_form' : otp_form,
		'validated' : status
	})

# Dashboard routes

@match_role("sponsor")
def dashboard(request):
	''' route for dashboard home '''

	u = Sponsor.objects.filter(user__email=request.session['email']).first()

	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsor
			exclude = ('user', 'users',)

	user_form = UserForm(instance=u.user)
	sponsor_form = SponsorForm(instance=u)
	errors = None

	if request.method == "POST":
		s = SponsorForm(request.POST, request.FILES, instance=u)
		u = UserForm(request.POST, request.FILES, instance=u.user)
		if s.is_valid() and u.is_valid():
			user = u.save(commit=False)
			ip_addr, del_val = getIP(request)
			print("IP ADDR : ", ip_addr)
			if ip_addr: user.last_IP = ip_addr
			user.save()
			sponsor = s.save(commit=False)
			sponsor.user = user
			sponsor.save()
		user_form = u
		sponsor_form = s
		errors = [u.errors, s.errors]
		print(errors)

	return render(request, 'sponsor/dashboard/index.html.j2', context={
		"title": "Dashboard Home",
		'user_form' : user_form,
		'sponsor_form' : sponsor_form,
		'errors' : errors,
		'sponsor': get_sponsor(request.session['email']),
	})

# @match_role("sponsor")
# def discounts(request):
# 	''' route for dashboard discounts '''

# 	u = Sponsor.objects.filter(user__email=request.session['email']).first()

# 	return render(request, 'sponsor/dashboard/discountcards.html.j2', context={
# 		'title' : "Discount cards",
# 		})

@match_role("sponsor")
def addUsers(request, file):
	'''
		takes in an excel file and returns
		the list of user objects, along with missed ones
		@param file -> excel file of users
		@return list of users, list of wrong

	'''
	users, invalid = [], []
	sh = xlrd.open_workbook(filename=None, file_contents=
		file.read()).sheet_by_index(0)
	data = [[sh.cell(r, c).value if sh.cell(r, c).value != '' else None for c
		in range(sh.ncols)] for r in range(sh.nrows)]

	update_date = datetime.datetime.now()
	ip_addr, del_val = getIP(request)
	questions = list(Question.objects.all())

	# class UserBulkForm(forms.Form):
	#   email = forms.CharField(max_length=150)
	#   name = forms.CharField(max_length=150)
	#   mobile = forms.CharField(validators=[
	#       RegexValidator(
	#           regex=r'^(\+\d{1,3}[- ]?)?\d{10}$',
	#           message="Invalid Number")], max_length=15)
	#   password = forms.CharField(max_length=100)
	#   gender = forms.CharField(max_length=1, choices=(
	#       ('M', 'Male'),
	#       ('F', 'Female'),
	#       ('O', 'Other'),))
	#   dob = forms.CharField(max_length=10)


	# fields => email, name, mobile, password, gender
	users_obj, seeker_obj = [], []
	for row, idx in zip(data[1:], range(sh.nrows)):
		if None in row:
			invalid.append(idx)
			continue
		fields = row[1:]
		data = {
			'email' : fields[0],
			'name' : fields[1],
			'mobile' : fields[2],
			'password' : make_password(fields[3]),
			'gender' : random.choice(['M', 'O', 'F']),
			'question': random.choice(questions),
			'answer' : fields[2],
			'profession' : 'other',
			'language' : 'english',
			'dob' : datetime.datetime.strptime(fields[4], '%Y-%m-%d').date(),
		}
		user = User(email=data['email'], name=data['name'],
			mobile=data['mobile'], password=data['password'],
			gender=data['gender'], role='healthseeker',
			last_IP=(ip_addr or '127.0.0.1'), last_update=datetime.datetime.now(),
			question=data['question'], answer=data['answer'])
		try:
			print("Saving user")
			user.save()
			users_obj.append(user)
			print("U :", users_obj[-1])
		except:
			invalid.append(idx)
			continue

		seeker = Seeker(profession=data['profession'], language=data['language'],
			dob=data['dob'], user=users_obj[-1])
		try:
			print("Saving seeker\n\n")
			seeker.save()
			seeker_obj.append(seeker)
			print("S : ", seeker_obj[-1])
		except:
			users_obj.pop()
			invalid.append(idx)
			continue

		# User.objects.bulk_create(users_obj)
		# seeker_obj.bulk_create(seeker_obj)
	return seeker_obj, invalid


@match_role("sponsor")
def user_view(request):
	'''
		route for adding and viewing users
		- Single user (new) addition (Seeker form)
		- Multiple (existing user additon) (Sponsor form only single field)
		- Excel based multiple (new) user addition (manually)
		- Viewing added users and modifying (formset factory)

	'''

	class SeekerForm(forms.ModelForm):
		class Meta:
			model = Seeker
			exclude = ('user', 'family',)

	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsor
			fields = ('users',)

		def __init__(self, *args, **kwargs):
			super(SponsorForm, self).__init__(*args, **kwargs)
			self.fields['users'].widget = forms.CheckboxSelectMultiple()
			self.fields['users'].queryset = Seeker.objects.all()

	class SeekerMultipleForm(forms.Form):
		file = forms.FileField()

		def is_valid(self):
			init_validity = super(SeekerMultipleForm, self).is_valid()
			if not init_validity: return init_validity
			f = self.cleaned_data['file']
			if f.name.rsplit('.')[-1] not in ['xlsx', 'xls']:
				print("hello error")
				self.add_error('file', "Invalid file")
				return False
			return True

	u = Sponsor.objects.filter(user__email=request.session['email']).first()
	errors = None

	class UserForm(forms.ModelForm):
		class Meta:
			model = User
			fields = ('email', 'name', 'mobile',)

	basic_user = UserForm()
	seeker_specific = SeekerForm()
	existing_multiple = SponsorForm(instance=u)
	bulk_form = SeekerMultipleForm()

	if request.method == "POST":
		# handle all the forms here
		# with error detection and particular routing
		errors = []

		if request.POST['type'] == "single_user":
			b = UserForm(request.POST, request.FILES)
			# s = SeekerForm(request.POST, request.FILES)
			# if b.is_valid() and s.is_valid():
			if b.is_valid():
				user = b.save(commit=False)
				ip_addr, del_val = getIP(request)
				user.role = 'healthseeker'
				user.password = make_password(user.mobile)
				user.question = Question.objects.first()
				user.answer = "default"
				user.save()
				# seeker = s.save(commit=False)
				seeker = Seeker(user=user, dob=datetime.datetime.now().date())
				seeker.user = user
				seeker.save()
				u.users.add(seeker)
			else:
				basic_user = b
				# seeker_specific = s
				errors += [b.errors]

		elif request.POST['type'] == "existing_multiple":
			# code for adding the multiple existing users
			# to the sponsor users_store
			s = SponsorForm(request.POST, request.FILES, instance=u)
			if s.is_valid():
				s.save()
			else:
				errors += [s.errors]
			existing_multiple = s

		elif request.POST['type'] == "new_multiple":
			# code to handle the multiple additon
			# from an excel sheet or something
			# MANUAL PARSING
			m = SeekerMultipleForm(request.POST, request.FILES)
			if m.is_valid():
				user_list, missed = addUsers(request, request.FILES['file'])
			else:
				errors += [m.errors]
				# print(errors)
			bulk_form = m

	# print("errors : ", errors)
	return render(request, 'sponsor/dashboard/participants/new.html.j2', context={
		'title' : "Participants",
		'sponsor': get_sponsor(request.session['email']),
		'errors' : errors,
		'basic_user' : basic_user,
		# 'seeker_specific': seeker_specific,
		# 'existing_multiple' : existing_multiple,
		'bulk_form' : bulk_form
	})

# new routes

# account details

@match_role("sponsor")
def account_basic(request):
	''' edit basic organizational and POC details '''

	s = Sponsor.objects.filter(user__email=request.session['email']).first()

	class OrgForm(forms.ModelForm):
		class Meta:
			model = Organization
			fields = ('name', 'type', 'size', 'image',)

	class POCForm(forms.ModelForm):
		class Meta:
			model = User
			fields = ('mobile', 'email',  'gender',)

	if request.method == "POST":
		org_form = OrgForm(request.POST, request.FILES, instance=s.organization)
		poc_form = POCForm(request.POST, request.FILES, instance=s.user)
		if org_form.is_valid(): org_form.save()
		if poc_form.is_valid():
			poc_form.save()
			request.session['email'] = s.user.email
	else:
		org_form = OrgForm(instance=s.organization)
		poc_form = POCForm(instance=s.user)

	return render(request, 'sponsor/dashboard/account/basic.html.j2', context={
		'title': 'Account - Basic Details',
		'sponsor': get_sponsor(request.session['email']),
		'org_form' : org_form,
		'poc_form' : poc_form,
	})


class POCTable(Datatable):
	class Meta:
		model = User
		exclude = ['IP', ]
		columns = ['id', 'mobile', 'name', 'email']
		ordering = ['-id']
		# cache_type = cache_types.DEFAULT
		structure_template = 'datatableview/bootstrap_structure.html'

class POCForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('__all__')
		widgets = {
			'password' : forms.PasswordInput()
		}

class POCTableView(DatatableView):
	model = User
	datatable_class = POCTable

	def get_context_data(self, **kwargs):
		poc_form = POCForm()

		context = super().get_context_data(**kwargs)
		context['title'] = 'POCs'
		context['sponsor'] = get_sponsor(self.request.session['email'])
		context['poc_form'] = poc_form
		return context

	def get_template_names(self):
		return 'sponsor/dashboard/account/contact.html.j2'

	def get_queryset(self):
		sp = get_sponsor(self.request.session['email'])
		return sp.pocs.all()

@match_role("sponsor")
def add_poc(request):
	if request.method  == "POST":
		poc = POCForm(request.POST, request.FILES)
		s = Sponsor.objects.filter(user__email=request.session['email']).first()

		if poc.is_valid():
			p = poc.save()
			s.pocs.add(p)
			s.save()
		else:
			# errors += [poc.errors]
			print('error in commiting')

	return redirect('sponsor:contact')

@match_role("sponsor")
def contact(request):
	if request.method == "POST":
		print(request)
		c_dict = parser.parse(request.POST.urlencode())
		print(c_dict)
	return render(request, 'sponsor/dashboard/account/contact.html.j2', context={
		'title': 'POC',
		'sponsor': get_sponsor(request.session['email']),
	})

@match_role("sponsor")
def account_organization(request):

	s = Sponsor.objects.filter(user__email=request.session['email']).first()
	message = None

	class OrganizationForm(forms.ModelForm):
		class Meta:
			model = Organization
			exclude = ('location',)

	if request.method == "POST":
		org_form = OrganizationForm(request.POST, request.FILES, instance=s.organization)
		if org_form.is_valid():
			org_form.save()
		location_obj = json.loads(request.POST['j_string'])
		full_name = location_obj['formatted_address']
		try:
			pos_loc = Location.objects.get(full_name__icontains=full_name)
			s.organization.location = pos_loc
			s.organization.save()
			message = 'Location found in database! (using exsiting)'
		except Exception as e:
			message = 'Location added to database!'
			try:
				pos_loc = Location(place=location_obj)
				pos_loc.save()
				s.organization.location = pos_loc
				s.organization.save()
			except Exception as e:
				message = 'Invalid location! (%s)' % str(e)
	else:
		org_form = OrganizationForm(instance=s.organization)

	try:
		location = s.organization.location.full_name
	except:
		location = None

	print(location, message)
	return render(request, 'sponsor/dashboard/account/organization.html.j2', context={
		'title': 'Account - Organization',
		'org_form' : org_form,
		'location' : location,
		'message' : message,
	})

# payments

class PaymentsTable(Datatable):
	class Meta:
		model = Transaction
		exclude = ['IP', ]
		# columns = ['id', 'mobile', 'name', 'email']
		ordering = ['-id']
		# cache_type = cache_types.DEFAULT
		structure_template = 'datatableview/bootstrap_structure.html'

class PaymentsTableView(DatatableView):
	model = Transaction
	datatable_class = PaymentsTable

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Payments - View'
		context['sponsor'] = get_sponsor(self.request.session['email'])
		return context

	def get_template_names(self):
		return 'sponsor/dashboard/payments/view.html.j2'

	def get_queryset(self):
		sp = get_sponsor(self.request.session['email'])
		return Transaction.objects.filter(receiver=sp.user)


@match_role("sponsor")
def payments_new(request):
	'''
		route to display catalog of new discount cards and payments

	'''

	if 'coupon' in request.session: del request.session['coupon']
	discounts = DiscountCard.objects.all()
	checkups = HealthCheckup.objects.all()

	return render(request, 'sponsor/dashboard/payments/new.html.j2', context={
		'title': 'Payments',
		'sponsor': get_sponsor(request.session['email']),
		'discounts': discounts,
		'checkups': checkups,
	})


@match_role("sponsor")
def payments_add(request, type, package_id):
	'''
		add a new payment once a package has been selected

	'''
	if type == "healthcheck":
		try:
			dis_type = HealthCheckup.objects.get(uid=package_id)
		except:
			raise Http404("Invalid UID")
	elif type == "discountcard":
		try:
			dis_type = DiscountCard.objects.get(uid=package_id)
		except:
			raise Http404("Invalid UID")
	else:
		raise Http404("Invalid Type")

	if request.method == "POST":
		if 'coupon' in request.session:
			print("C : ", request.session['coupon'])
		p_data = parser.parse(request.POST.urlencode())
		request.session['users'] = p_data['can_id']
		request.session['pack_type'] = type
		request.session['pack_id'] = dis_type.id
		return redirect('common:payment_init')

	sponsor = get_sponsor(request.session['email'])
	candidates = [_.user for _ in sponsor.users.all()]
	fields = ('pk', 'email', 'name', 'mobile', 'gender',)
	candidates = serializers.serialize("python", candidates, fields=fields)

	return render(request, 'sponsor/dashboard/payments/add.html.j2', context={
		'title': 'Payments',
		'sponsor': sponsor,
		'candidates' : candidates,
		'card' : dis_type,
		'fields' : fields
	})


# participants

class ParticipantsTable(Datatable):
	class Meta:
		model = User
		exclude = ['last_IP', 'password', 'question',]
		columns = ['id', 'mobile', 'name', 'email']
		ordering = ['-id']
		# cache_type = cache_types.DEFAULT
		structure_template = 'datatableview/bootstrap_structure.html'

class ParticipantsTableView(DatatableView):
	model = User
	datatable_class = ParticipantsTable

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Participants - View'
		context['sponsor'] = get_sponsor(self.request.session['email'])
		return context

	def get_template_names(self):
		return 'sponsor/dashboard/participants/view.html.j2'

	def get_queryset(self):
		sp = get_sponsor(self.request.session['email'])
		return User.objects.filter(seeker__in=sp.users.all())

@match_role("sponsor")
def participants_new(request):

	return render(request, 'sponsor/dashboard/participants/new.html.j2', context={
		'title': 'Participants',
		'sponsor': get_sponsor(request.session['email']),
	})
