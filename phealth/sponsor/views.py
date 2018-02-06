from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from django import forms
from api.models import Sponsors
# Create your views here.

# sponsor common routes


def SignUp(request):
	if request.method == "GET":
		return render(request, 'sponsor/registration.html.j2', context={
			'route': "/sponsor"
		})
	elif request.method == "POST":
		print("Posting data")
		print(request.POST)
		print(request.FILES)
		return JsonResponse({'status': True})


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

	class BasicForm(forms.ModelForm):

		class Meta:
			model = Sponsors
			fields = ('__all__')

	if request.method == "POST":
		b = BasicForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()

	return render(request, 'sponsor/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit basic information",
		"form" : BasicForm(instance=u)
	})


@match_role("sponsor")
def organization(request):
	''' route for dashboard  organizations'''
	return render(request, 'sponsor/dashboard/organization.html.j2', context={
		"title": "Dashboard - Organization details"
	})


@match_role("sponsor")
def education(request):
	''' route for dashboard education'''
	return render(request, 'sponsor/dashboard/education.html.j2', context={
		"title": "Dashboard - education details "
	})


@match_role("sponsor")
def contact(request):
	''' route for dashboard  contact details'''
	return render(request, 'sponsor/dashboard/contact.html.j2', context={
		"title": "Dashboard - contact details "
	})


@match_role("sponsor")
def business(request):
	''' route for dashboard business '''
	return render(request, 'sponsor/dashboard/business.html.j2', context={
		"title": "Dashboard - business details "
	})


@match_role("sponsor")
def participants(request):
	''' route for dashboard participants'''
	return render(request, 'sponsor/dashboard/participants.html.j2', context={
		"title": "Dashboard - participants details "
	})


@match_role("sponsor")
def discounts(request):
	''' route for dashboard discounts '''
	return render(request, 'sponsor/dashboard/discounts.html.j2', context={
		"title": "Dashboard - discounts details "
	})
