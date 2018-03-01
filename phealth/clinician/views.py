
from django import forms
from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from api.models import (Clinician, User, Speciality, Appointment  )
from querystring_parser import parser
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
	''' no signin functionality for the clinician
	'''
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
			fields = ('name', 'email', 'mobile', 'gender',
			 'question', 'answer', 'profile_pic')

	if request.method == "POST":
		c = ClinicianForm(request.POST, request.FILES, instance=u)
		b = UserForm(request.POST, request.FILES, instance=v)
		if c.is_valid() and b.is_valid():
			c.save() and b.save()

	return render(request, 'clinician/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit basic information",
		"clinician_form" : ClinicianForm(instance=u),
		"user_form" : UserForm(instance=v),
	})

@match_role("clinician")
def speciality(request):
	u = Clinician.objects.filter(user__email=request.session['email']).first()
	n = u.specialities.all()
	print("I was here")
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
	apps = Appointment.objects.filter(under=c).all().order_by('id')
	appointments_arr = []
	class AppointmentForm(forms.ModelForm):

		class Meta:
			model = Appointment
			fields = ('status',)


	for appointment in apps:
	 	appointments_arr.append((appointment, AppointmentForm(instance=appointment)))


	if request.method == 'POST':
		print(request.POST)
		b = AppointmentForm(request.POST, request.FILES, instance=Appointment.objects.filter(id=int(request.POST['appointment'])).first())
		if b.is_valid():
			b.save()
			print(b)

	return render(request, 'clinician/dashboard/appointments.html.j2', context={
		"title": "Doctors Appointment List",
		"appointments": appointments_arr,
		})


@match_role("clinician")
def calender(request):
	''' dashboard function '''
	''' handles the calender page for clincian timings
	and bookings
	'''
	c = Clinician.objects.filter(user__email=request.session['email']).first()
	days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

	if request.method == "POST":
		p_dict = parser.parse(request.POST.urlencode())
		if p_dict['section'] in ['work', 'break']:
			timings = []
			if p_dict['section'] == 'work': base_compare = c.work_timings
			else: base_compare = c.break_timings
			for day, actual in zip(days, base_compare):
				try:
					timings.append(list(map(lambda x: datetime.datetime.strptime(x,
					 '%H:%M:%S').time(), p_dict['timings'][day])))
				except ValueError:
					try:
						timings.append(list(map(lambda x: datetime.datetime.strptime(x,
					 	'%H:%M').time(), p_dict['timings'][day])))
					except KeyError:
						timings.append(actual)
				except KeyError:
					timings.append(actual)
			if p_dict['section'] == 'work':
				c.work_timings = timings
			else:
				c.break_timings = timings
		else:
			try:
				vacs = p_dict['timings'][""]
				vacs = [ list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
				 [i, j])) for i, j in zip(vacs[::2], vacs[1::2])]
				c.vacations = vacs
			except:
				pass
		c.save()

	work_timings, break_timings, vacation_timings = [], [], []

	for day, w_t, b_t in zip(days, c.work_timings, c.break_timings):
		cur_obj = { 'day' : day }
		cur_obj['start'] = w_t[0].isoformat().split('.')[0][:5]
		cur_obj['end'] = w_t[-1].isoformat().split('.')[0][:5]
		work_timings.append(cur_obj)
		cur_obj['start'] = b_t[0].isoformat().split('.')[0][:5]
		cur_obj['end'] = b_t[-1].isoformat().split('.')[0][:5]
		break_timings.append(cur_obj)

	for vacation in c.vacations:
		vacation_timings.append({
			'start' : vacation[0].isoformat(),
			'end' : vacation[-1].isoformat(),
		})

	return render(request, 'clinician/dashboard/calender.html.j2', context={
			'title' : "Set your timings",
			'work' : work_timings,
			'break' : break_timings,
			'vacations' : vacation_timings,
		})
