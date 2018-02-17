
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
	n = u.specialities.all()
	class SpecialityForm(forms.ModelForm):
		class Meta:
			model = Speciality
			fields = ('name', 'description',)
	v = SpecialityForm()
	if request.method == "POST":
		b = SpecialityForm(request.POST, request.FILES)
		if b.is_valid():
			u.save()
			speciality = b.save(commit=False)
			u.specialities.add(speciality)
		else:
			v = b

	return render(request, 'clinician/dashboard/speciality.html.j2', context={
	 	"title": "Speciality Addition", 
	 	"speciality_form" : v,
	 	"speciality_list" : n,
	})


# @match_role("clinician")
def appointments(request):
	c = Clinician.objects.filter(user__email=request.session['email']).first()
	apps = Appointment.objects.filter(under=c).all()
	return render(request, 'clinician/dashboard/appointments.html.j2', context={
		"title": "Doctors Appointment List",
		"appointments": apps
		})

# @match_role("clinician")
def calender(request):
	''' dashboard function '''
	''' handles the calender page for clincian timings
	and bookings
	'''
	c = Clinician.objects.filter(user__email=request.session['email']).first()
	work_timings = c.work_timings
	break_timings = c.break_timings
	vacations = c.vacations
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

