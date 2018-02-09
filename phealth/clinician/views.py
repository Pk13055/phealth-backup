from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
import datetime

# Create your views here.


def SignUp(request):
	if request.method == "GET":
		return render(request, 'clinician/registration.html.j2', context={
			'route': "/clinician",
			'title': "Clinician Sign up"
			})
	elif request.method == "POST":
		print("Posting data")
		print(request.POST)
		print(request.FILES)
		return JsonResponse({'status' : True })


def SignIn(request):
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Clinician Login",
			"route": "/clinician",
			"color": "info"
		})
	elif request.method == "POST":
		if signin("clinician", request):
			return redirect('clinician:dashboard')
		return redirect('clinician:signin')


# Dashboard view functions



@match_role("sponsor")
def dashboard(request):
	''' route for dashboard home '''

	u = Clinician.objects.filter(users__email=request.session['email']).first()

	class BasicForm(forms.ModelForm):

		class Meta:
			model = Clinician
			fields = ('__all__')

	if request.method == "POST":
		b = BasicForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()

	return render(request, 'clinician/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit basic information",
		"form" : BasicForm(instance=u)
	})


@match_role("clinician")
def personal_info(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/home.html.j2', context={
		'title' : "Clinician Dashboard"
		})

@match_role("clinician")
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

@match_role("clinician")
def professional_info(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/profesional.html.j2', context={
		"title" : "Dashboard - Professional Information"
		})

@match_role("clinician")
def education_training(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/education.html.j2', context={
		"title" : "Dashboard - education_training"
		})

@match_role("clinician")
def consultation_fee(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/consulation.html.j2', context={
		"title" : "Dashboard - consultation_fee"
		})

@match_role("clinician")
def offerings(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/offerings.html.j2', context={
		"title" : "Dashboard - offerings"
		})

@match_role("clinician")
def conditions_treated(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/conditions.html.j2', context={
		"title" : "Dashboard - conditions_treated"
		})

@match_role("clinician")
def experience(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/experience.html.j2', context={
		"title" : "Dashboard - experience"
		})

@match_role("clinician")
def award_recognition(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/awards.html.j2', context={
		"title" : "Dashboard - award_recognition"
		})

@match_role("clinician")
def registrations(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/registrations.html.j2', context={
		"title" : "Dashboard - registrations"
		})

@match_role("clinician")
def membership(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/membership.html.j2', context={
		"title" : "Dashboard - membership"
		})

@match_role("clinician")
def areas_of_interest(request):
	''' dashboard function '''
	return render(request, 'clinician/dashboard/interest.html.j2', context={
		"title" : "Dashboard - areas_of_interest"
		})
