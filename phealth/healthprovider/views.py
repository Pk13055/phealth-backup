import random

from django.shortcuts import render
from phealth.utils import match_role, signin, redirect
from django.http import JsonResponse
from django import forms
from django.contrib.auth.hashers import make_password
from api.models import (User, Provider, Speciality,
	Clinician, Appointment)

# Create your views here.

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('__all__')

def SignUp(request):

	class ProviderForm(forms.ModelForm):

		class Meta:
			model = Provider
			exclude = ('poc', 'specialities', 'active_from')

	if request.method == "POST":
		print(request.POST, request.FILES)
		p = ProviderForm(request.POST, request.FILES)
		u = UserForm(request.POST, request.FILES)
		print(p.is_valid(), u.is_valid())
		print(request.session['otp'], request.POST['otp'])
		if p.is_valid() and u.is_valid() and \
			str(request.POST['otp']) == str(request.session['otp']):
			user = u.save(commit=False)
			ip_addr, del_val = getIP(request)
			if ip_addr: user.last_IP = ip_addr
			user.role = 'healthprovider'
			user.password = make_password(user.password)
			user.save()
			provider = p.save(commit=False)
			provider.poc = user
			provider.save()
			del request.session['otp']
			return redirect('healthprovider:signin')
		user_form = u
		provider_form = p
		errors = [u.errors, p.errors, "OTP did not match!"]
		print(errors)

	elif request.method == "GET":
		user_form = UserForm()
		provider_form = ProviderForm()
		errors = None

	if 'otp' not in request.session:
		request.session['otp'] = random.randint(1, 9999)

	return render(request, 'healthprovider/registration.html.j2', context={
		'title' : "Healthprovider Registration",
		'route': "/healthprovider",
		'user_form' : user_form,
		'sponsor_form' : provider_form,
		'errors' : errors
	})

def SignIn(request):
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title" : "Healthprovider Login",
			"route" : "/healthprovider",
			"color" : "primary"
			})
	elif request.method == "POST":
		if signin("healthprovider", request):
			return redirect('healthprovider:dashboard_home')
		return redirect('healthprovider:signin')

@match_role("healthprovider")
def dashboard(request):
	''' route for dashboard home '''

	p = Provider.objects.filter(poc__email=request.session['email']).first()

	if request.method == "POST":
		u = UserForm(request.POST, request.FILES, instance=p.poc)
		if u.is_valid():
			u.save()
		print(u)

	return render(request, 'healthprovider/dashboard/home.html.j2', context={
		"title": "Home",
		"form_title" : "Edit Basic Information",
		"form" : UserForm(instance=p.poc)
	})

@match_role("healthprovider")
def branches(request):
	''' route for provider branches '''

	return JsonResponse({"status": True})

@match_role("healthprovider")
def specialities(request):
	''' route for provider specialities '''

	p = Provider.objects.filter(poc__email=request.session['email']).first()

	class SpecialityForm(forms.ModelForm):
		class Meta:
			model = Speciality
			fields = ('__all__')

	class ProviderForm(forms.ModelForm):
		class Meta:
			model = Provider
			fields = ('specialities',)

		def __init__(self, *args, **kwargs):
			super(ProviderForm, self).__init__(*args, **kwargs)
			self.fields['specialities'].widget = forms.CheckboxSelectMultiple()
			self.fields['specialities'].queryset = Speciality.objects.all()

	edit_form = ProviderForm(instance=p)

	if request.method == "POST":
		if request.POST['type'] == 'add':
			s = SpecialityForm(request.POST, request.FILES).save(commit=False)
			s.save()
			p.specialities.add(s)

		if request.POST['type'] == 'edit':
			h = ProviderForm(request.POST, request.FILES, instance=p)
			if h.is_valid():
				h.save()
			else:
				errors += [h.errors]
			edit_form = h

	return render(request, 'healthprovider/dashboard/speciality.html.j2', context={
		"title": "Specialities",
		"form" : SpecialityForm(),
		"edit_form": edit_form,
	})

@match_role("healthprovider")
def clinicians(request):
	''' route for provider clinicians '''

	p = Provider.objects.filter(poc__email=request.session['email']).first()

	class ClinicianForm(forms.ModelForm):
		class Meta:
			model = Clinician
			exclude = ('work_timings', 'break_timings', 'vacations', 'experience', 'user')

	class ProviderForm(forms.ModelForm):
		class Meta:
			model = Provider
			fields = ('clinicians',)

		def __init__(self, *args, **kwargs):
			super(ProviderForm, self).__init__(*args, **kwargs)
			self.fields['clinicians'].widget = forms.CheckboxSelectMultiple()
			self.fields['clinicians'].queryset = p.clinicians.all()

	edit_form = ProviderForm(instance=p)

	if request.method == "POST":
		if request.POST['type'] == 'add':
			u = UserForm(request.POST, request.FILES).save(commit=False)
			u.password = make_password(u.password)
			u.save()
			c = ClinicianForm(request.POST, request.FILES).save(commit=False)
			c.user = u
			c.save()
			p.clinicians.add(c)

		if request.POST['type'] == 'edit':
			h = ProviderForm(request.POST, request.FILES, instance=p)
			if h.is_valid():
				h.save()
			else:
				errors += [h.errors]
			edit_form = h

	return render(request, 'healthprovider/dashboard/clinician.html.j2', context={
		"title": "Clinicians",
		"form_user": UserForm(),
		"form_clinician": ClinicianForm(),
		"form_clinician_edit": edit_form,
	})

@match_role("healthprovider")
def appointments(request):
	''' route for dahsboard doctors list '''

	p = Provider.objects.filter(poc__email=request.session['email']).first()
	states = [('pending', 'warning'), ('confirmed', 'success'), ('cancelled', 'danger'), ('rescheduled', 'info')]

	appointments = {}
	for state in states:
		appointments[state[0]] = {
			'queryset': p.appointment_set.filter(status=state[0]).order_by('date', 'time').all(),
			'color': state[1],
		}

	return render(request, 'healthprovider/dashboard/appointment.html.j2', context={
		"title": "Appointment List",
		"appointments": appointments.items(),
	})
