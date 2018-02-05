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


@match_role("clinician")
def dashboard(request):
	return JsonResponse({'status' : True })

@match_role("clinician")
def calender(request):
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
		return render(request, 'clinician/calender.html.j2', context={
			'title' : "Set your timings",
			'days' : schedule
			})
	elif request.method == "POST":
		print("Form submitted for update")
		print(request.POST)
		return JsonResponse({ 'status' : True })
