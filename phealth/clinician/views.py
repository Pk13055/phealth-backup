
from django import forms
from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from api.models import (Clinician, User, Speciality, Appointment  )
#  CliniciansExperience, CliniciansSpeciality)
import datetime


# Create your views here.

def SignIn(request):
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Clinician Login",
			"route": "/clinician",
			"color": "info"
		})
	elif request.method == "POST":
		if signin("clinician", request):
			return redirect('clinician:dashboard_home')
		return redirect('clinician:signin')


# Dashboard view functions

@match_role("clinician")
def dashboard(request):
	''' route for dashboard home '''

	u = Clinician.objects.filter(user__email=request.session['email']).first()
	v = u.user 
	class ClinicianForm(forms.ModelForm):

		class Meta:
			model = Clinician
			fields = ('education', 'experience') 
	class UserForm(forms.ModelForm):

		class Meta:
			model = User
			fields = ('name', 'email', 'mobile', 'gender', 'question', 'answer', 'profile_pic')

	if request.method == "POST":
		c = ClinicianForm(request.POST, request.FILES, instance=u)
		b = UserForm(request.POST, request.FILES, instance=u)
		if c.is_valid() and b.is_valid():
			c.save()
			b.save()

	return render(request, 'clinician/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit basic information",
		"clinician_form" : ClinicianForm(instance=u),
		"user_form" : UserForm(instance=v),
	})

# @match_role("clincian")
def speciality(request):
	u = Clinician.objects.filter(user__email=request.session['email']).first()
	class SpecialityForm(forms.ModelForm):
		class Meta:
			model = Speciality
			fields = ('name', 'description',)

	v = SpecialityForm()
	
	if request.method == "POST":
		b = SpecialityForm(request.POST, request.FILES)
		if b.is_valid():
			speciality = b.save(commit=False)
			u.specialities.add(speciality)
			u.save()
		else:
			v = b

	return render(request, 'clinician/dashboard/speciality.html.j2', context={
	 	"title": "Speciality Addition", 
	 	"speciality_form" : v
	})


# @match_role("clinician")
def appointments(request):
	
	return render(request, 'clinician/dashboard/appointments.html.j2', context={
		"title": "Doctors Appointment List",})

# @match_role("clinician")
# def education_training(request):
# 	''' handles the edit and update of education details
# 	'''
# 	u = Clinicians.objects.filter(users__email=request.session['email']).first()
# 	e = CliniciansEducation.objects.filter(clinicians=u).first()

# 	class EducationForm(forms.ModelForm):

# 		class Meta:
# 			model = CliniciansEducation
# 			exclude = ('clinicians',)


# 	if request.method == "POST":
# 		c = EducationForm(request.POST, request.FILES, instance=e)
# 		if c.is_valid():
# 			d = c.save(commit=False)
# 			d.clinicians = u
# 			d.save()
# 	else:
# 		e = CliniciansEducation.objects.filter(clinicians=u).first()

# 	return render(request, 'clinician/dashboard/education.html.j2', context={
# 		'title' : "Clinician - details",
# 		'form_title' : "Education Details",
# 		'form' : EducationForm(instance=e)
# 		})

# @match_role("clinician")
def calender(request):
	''' dashboard function '''
	''' handles the calender page for clincian timings
	and bookings
	'''
	if request.method == "GET":
		schedule = []
		for day in ["Sunday", "Monday",
		 "Tuesday", "Wednesday", "Friday", "Saturday"]:
		 	cur_day = {
		 		'day' : day,
		 		'start' : datetime.datetime.now().time(),
		 		'end' : datetime.datetime.now().time(),
		 	}
		 	schedule.append(cur_day)
		return render(request, 'clinician/dashboard/calender.html.j2', context={
			'title' : "Set your timings",
			'days' : schedule
			})
	elif request.method == "POST":
		print("Form submitted for update")
		print(request.POST)
		return JsonResponse({ 'status' : True })

# @match_role("clinician")
# def conditions(request):
# 	''' handles the edit and addition of conditions details
# 	'''
# 	u = Clinicians.objects.filter(users__email=request.session['email']).first()

# 	class CliniciansSpecialityForm(forms.ModelForm):

# 		class Meta:
# 			model = CliniciansSpeciality
# 			exclude = ('clinicians', 'reg_date', 'healthproviders_speciality',)
# 			widgets = {
# 				'activefrom' : forms.TextInput(attrs={ 'placeholder' : "YYYY-MM-DD" }),
# 				'activeto' : forms.TextInput(attrs={ 'placeholder' : "YYYY-MM-DD" }),
# 			}

# 	EditFormSet = forms.modelformset_factory(CliniciansSpeciality, form=CliniciansSpecialityForm, extra=0)

# 	if request.method == "POST":
# 		_forms = []
# 		if request.POST['data_type'] == "add":
# 			c = CliniciansSpecialityForm(request.POST, request.FILES)
# 			_forms.append(c)
# 		elif request.POST['data_type'] == "update":
# 			c = EditFormSet(request.POST, request.FILES)
# 			_forms += c.forms

# 		for form in _forms:
# 			if form.is_valid():
# 				d = form.save(commit=False)
# 				d.clinicians = u
# 				d.save()
# 			else:
# 				print("errors :", form.errors)

# 	return render(request, 'clinician/dashboard/conditions.html.j2', context={
# 		'title' : "Clinician - Conditions treated",
# 		'form_title': "Add conditions treated",
# 		'form' : CliniciansSpecialityForm(),
# 		'edit_forms' : EditFormSet(queryset=CliniciansSpeciality.objects.filter(clinicians=u))
# 			})

# @match_role("clinician")
# def surgeries(request):
# 	''' handles the edit and addition of surgeries performed
# 	'''
# 	u = Clinicians.objects.filter(users__email=request.session['email']).first()

# 	class CliniciansExperienceForm(forms.ModelForm):

# 		class Meta:
# 			model = CliniciansExperience
# 			exclude = ('clinicians', 'reg_date')
# 			widgets = {
# 				'workfrom' : forms.TextInput(attrs={ 'placeholder' : "YYYY-MM-DD" }),
# 				'workto' : forms.TextInput(attrs={ 'placeholder' : "YYYY-MM-DD" }),
# 			}

# 	EditFormSet = forms.modelformset_factory(CliniciansExperience, form=CliniciansExperienceForm, extra=0)

# 	if request.method == "POST":
# 		_forms = []
# 		if request.POST['data_type'] == "add":
# 			c = CliniciansExperienceForm(request.POST, request.FILES)
# 			_forms.append(c)
# 		elif request.POST['data_type'] == "update":
# 			c = EditFormSet(request.POST, request.FILES)
# 			_forms += c.forms

# 		for form in _forms:
# 			if form.is_valid():
# 				d = form.save(commit=False)
# 				d.clinicians = u
# 				d.save()
# 			else:
# 				print("errors :", form.errors)

# 	return render(request, 'clinician/dashboard/surgeries.html.j2', context={
# 		'title' : "Clinician - Surgeries performed",
# 		'form_title': "Add surgeries performed",
# 		'form' : CliniciansExperienceForm(),
# 		'edit_forms' : EditFormSet(queryset=CliniciansExperience.objects.filter(clinicians=u))
# 		})

# @match_role("clinician")
# def membership(request):
# 	''' handles the edit and addition of conditions details
# 	'''
# 	u = Clinicians.objects.filter(users__email=request.session['email']).first()

# 	if request.method == "POST":
# 		# add update part here
# 		pass

# 	return render(request, 'clinician/dashboard/members.html.j2', context={
# 		'title' : "Clinician - Manage members",
# 		'form_title' : "Add new member"
# 		})

