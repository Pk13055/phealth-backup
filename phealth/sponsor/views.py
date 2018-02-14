from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from django import forms
from api.models import User, Sponsor
import random

# Create your views here.

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('__all__')
		# exclude = ()

# sponsor common routes
def SignUp(request):

	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsor
			exclude = ('user',)

	if request.method == "GET":

		user_form = UserForm()
		sponsor_form = SponsorForm()

		if 'otp' not in request.session:
			request.session['otp'] = random.randint(1, 9999)

		print("SESSION : ", request.session['otp'])

		return render(request, 'sponsor/new_reg.html.j2', context={
			'route': "/sponsor",
			'user_form' : user_form,
			'sponsor_form' : sponsor_form
		})

	elif request.method == "POST":
		if request.POST['otp'] != request.session['otp']:
			return JsonResponse({'status': False })
		sponsor = SponsorForm(request.POST, request.FILES)
		user = UserForm(request.POST, request.FILES)
		if user.is_valid() and sponsor.is_valid():
			print("Valid Data")
			u = user.save()
			s = sponsor.save(commit=False)
			s.user = user
			s.save()
			del request.session['otp']
		else:
			return render(request, 'sponsor/new_reg.html.j2', context={
				'route' : "/sponsor",
				'user_form' : user,
				'sponsor_form' : sponsor,
				'errors' : [user.errors, sponsor.errors]
				})


def SignIn(request):
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


# Dashboard routes

@match_role("sponsor")
def dashboard(request):
	''' route for dashboard home '''

	u = Sponsors.objects.filter(users__email=request.session['email']).first()

	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsors
			exclude = ('users', 'image', 'activefrom', 'activeto',)


	if request.method == "POST":
		b = SponsorForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()

	return render(request, 'sponsor/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit basic information",
		"form" : SponsorForm(instance=u)
	})


# @match_role("sponsor")
# def participants(request):
# 	''' route for dashboard participants'''
# 	if request.method == "POST":
# 		pass
# 		# handle the form parsing and data etc here

# 	return render(request, 'sponsor/dashboard/participants.html.j2', context={
# 		"title": "Dashboard - participants details "
# 	})


@match_role("sponsor")
def discounts(request):
	''' route for dashboard discounts '''

	u = Sponsors.objects.filter(users__email=request.session['email']).first()

	class DiscountForm(forms.ModelForm):
		class Meta:
			model = Coupons
			exclude = ('applicablesponsor', 'uniquecode',)
			widgets = {
				'validity' : forms.TextInput(attrs={
					'placeholder' : "YYYY-MM-DD"
					})
			}

	EditFormSet = forms.modelformset_factory(Coupons, exclude=('applicablesponsor',
		'uniquecode',), extra=0)

	if request.method == "POST":
		_forms = []
		if request.POST['data_type'] == "add":
			c = DiscountForm(request.POST, request.FILES)
			_forms.append(c)
		elif request.POST['data_type'] == "update":
			c = EditFormSet(request.POST, request.FILES)
			_forms += c.forms

		for form in _forms:
			if form.is_valid():
				d = form.save(commit=False)
				d.applicablesponsor = u.users.users_id
				d.save()
			else:
				print("errors :", form.errors)


	edit_forms = EditFormSet(queryset=Coupons.objects.filter(applicablesponsor=u.users.users_id))
	return render(request, 'sponsor/dashboard/discounts.html.j2', context={
		"title": "Dashboard - discounts details",
		"form" : DiscountForm(),
		"edit_forms": edit_forms
	})
