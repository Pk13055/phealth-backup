from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from django import forms
from phealth.utils import getIP
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

	u = Sponsor.objects.filter(user__email=request.session['email']).first()

	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsor
			exclude = ('user',)


	if request.method == "POST":
		b = SponsorForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()

	return render(request, 'sponsor/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit basic information",
		"form" : SponsorForm(instance=u)
	})


@match_role("sponsor")
def discounts(request):
	''' route for dashboard discounts '''

	u = Sponsor.objects.filter(user__email=request.session['email']).first()

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
				d.applicablesponsor = u.user.user_id
				d.save()
			else:
				print("errors :", form.errors)


	edit_forms = EditFormSet(queryset=Coupons.objects.filter(applicablesponsor=u.user.user_id))
	return render(request, 'sponsor/dashboard/discounts.html.j2', context={
		"title": "Dashboard - discounts details",
		"form" : DiscountForm(),
		"edit_forms": edit_forms
	})
