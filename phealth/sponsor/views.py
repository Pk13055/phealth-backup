import random
import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from django.contrib.auth.hashers import make_password
from django import forms
from django.core.files import File

from phealth.utils import getIP
from api.models import User, Sponsor, Seeker, Question

import xlrd

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
		if signin("sponsor", request):
			return redirect('sponsor:dashboard_home')
		return redirect('sponsor:signin')


def SignUp(request):
	''' route for the signup of a new sponsor
	'''
	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsor
			exclude = ('user',)

	if request.method == "POST":
		print(request.POST, request.FILES)
		s = SponsorForm(request.POST, request.FILES)
		u = UserForm(request.POST, request.FILES)
		print(s.is_valid(), u.is_valid())
		print(request.session['otp'], request.POST['otp'])
		if s.is_valid() and u.is_valid() and \
			str(request.POST['otp']) == str(request.session['otp']):
			user = u.save(commit=False)
			ip_addr, del_val = getIP(request)
			if ip_addr: user.last_IP = ip_addr
			user.role = 'sponsor'
			user.save()
			sponsor = s.save(commit=False)
			sponsor.user = user
			sponsor.save()
			del request.session['otp']
			return redirect('sponsor:signin')
		user_form = u
		sponsor_form = s
		errors = [u.errors, s.errors, "OTP did not match!"]
		print(errors)

	elif request.method == "GET":
		user_form = UserForm()
		sponsor_form = SponsorForm()
		errors = None

	if 'otp' not in request.session:
		request.session['otp'] = random.randint(1, 9999)

	return render(request, 'sponsor/registration.html.j2', context={
		'title' : "Sponsor Registration",
		'route': "/sponsor",
		'user_form' : user_form,
		'sponsor_form' : sponsor_form,
		'errors' : errors
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

	return render(request, 'sponsor/dashboard/basic_details.html.j2', context={
		"title": "Basic details",
		'user_form' : user_form,
		'sponsor_form' : sponsor_form,
		'errors' : errors
	})


@match_role("sponsor")
def discounts(request):
	''' route for dashboard discounts '''

	u = Sponsor.objects.filter(user__email=request.session['email']).first()

	return render(request, 'sponsor/dashboard/discountcards.html.j2', context={
		'title' : "Discount cards",
		})


def addUsers(file, request):
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

	# fields => email, name, mobile, password, gender
	users_obj, seeker_obj = [], []
	for row, idx in zip(data, range(sh.nrows)):
		if None in row:
			print(idx)
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
			'dob' : fields[4],
		}

		users_obj.append(User(email=data['email'], name=data['name'],
			mobile=data['mobile'], password=data['password'],
			gender=data['gender'], role='healthseeker',
			last_IP=(ip_addr or '127.0.0.1'), last_update=datetime.datetime.now()))
		seeker_obj.append(Seeker(profession=data['profession'], language=data['language'],
			dob=data['dob'], user=users_obj[-1]))
		try:
			users_obj[-1].save()
			seeker_obj[-1].save()
		except:
			invalid.append(idx)

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
				self.add_error('file', "Invalid file")
				return False
			return True



	u = Sponsor.objects.filter(user__email=request.session['email']).first()
	errors = None
	basic_user = UserForm()
	seeker_specific = SeekerForm()
	existing_multiple = SponsorForm(instance=u)
	bulk_form = SeekerMultipleForm()

	if request.method == "POST":
		# handle all the forms here
		# with error detection and particular routing
		print(request.POST)
		errors = []

		if request.POST['type'] == "single_user":
			b = UserForm(request.POST, request.FILES)
			s = SeekerForm(request.POST, request.FILES)
			if b.is_valid() and s.is_valid():
				user = b.save(commit=False)
				ip_addr, del_val = getIP(request)
				user.role = 'healthseeker'
				user.password = make_password(user.password)
				user.save()
				seeker = s.save(commit=False)
				seeker.user = user
				seeker.save()
			else:
				basic_user = b
				seeker_specific = s
				errors += [b.errors, s.errors]

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
				user_list, missed = addUsers(request.FILES['file'], request)
			else:
				errors += [m.errors]
			bulk_form = m

	print("errors : ", errors)
	return render(request, 'sponsor/dashboard/users.html.j2', context={
		'title' : "Add Seeker",
		'errors' : errors,
		'single_user' : {
			'basic_user' : basic_user,
			'seeker_specific': seeker_specific
			},
		'existing_multiple' : existing_multiple,
		'bulk_form' : bulk_form
		})
