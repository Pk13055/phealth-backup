
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

def SignUp(request):
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

@match_role("clincian")
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
			speciality = b.save()
			# speciality.save()
			u.specialities.add(speciality)
		else:
			v = b

	return render(request, 'clinician/dashboard/speciality.html.j2', context={
	 	"title": "Speciality Addition", 
	 	"speciality_form" : v,
	 	"speciality_list" : n,
	})


@match_role("clinician")
def appointments(request):
	c = Clinician.objects.filter(user__email=request.session['email']).first()
	apps = Appointment.objects.filter(under=c).all()
	return render(request, 'clinician/dashboard/appointments.html.j2', context={
		"title": "Doctors Appointment List",
		"appointments": apps
		})

@match_role("clinician")
def calender(request):
	''' dashboard function '''
	''' handles the calender page for clincian timings
	and bookings
	'''

	c = Clinician.objects.filter(user__email=request.session['email']).first()
		
	if request.method == "POST":
		print("Form submitted for update")
		v = request.POST['section']
		l = [[x, y] for x, y in zip(request.POST.getlist('start_time[]'), request.POST.getlist('end_time[]'))]	

		if v in ['work', 'break']:
			l = [list(map(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time(), _)) for _ in l]
		else:
			l = [list(map(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d').date(), _)) for _ in l]

		print(l)
		if v == 'work':
			c.work_time = l
		if v == 'break':
			c.break_time = l
		if v == 'vacation':
			c.vacation = l

		print(c.work_timings)
		c.save()
		print(c.work_timings)

	work_timings = c.work_timings
	break_timings = c.break_timings
	Vacations = c.vacations


	schedule = []
	schedule1 = []
	vacation = []

	days = ["Sunday", "Monday",
	 "Tuesday", "Wednesday", "Friday", "Saturday"]

	for day, timings in zip(days, work_timings):
	 	cur_day = {
	 		'day' : day,
	 		'start' : timings[0].isoformat()[:-7],
	 		'end' : timings[-1].isoformat()[:-7],
	 	}
	 	schedule.append(cur_day)

	for day, timings in zip(days, break_timings):
	 	cur_day = {
	 		'day' : day,
	 		'start' : timings[0].isoformat()[:-7],
	 		'end' : timings[-1].isoformat()[:-7],
	 	}
	 	schedule1.append(cur_day)

	for v in Vacations:
	 	cur_vacation = {
	 		'start_day' : v[0].isoformat(),
	 		'end_day'   : v[1].isoformat(),
	 	}
	 	vacation.append(cur_vacation)

	return render(request, 'clinician/dashboard/calender.html.j2', context={
			'title' : "Set your timings",
			'work_days' : schedule,
			'break_days' : schedule1,
			'vacation_days' : vacation,
			})

