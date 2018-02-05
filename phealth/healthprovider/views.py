from django.shortcuts import render
from phealth.utils import match_role
from django.http import JsonResponse
# Create your views here.


def SignUp(request):
	if request.method == "GET":
		return render(request, 'healthprovider/registration.html.j2', context={ 'route': "/healthprovider" })
	elif request.method == "POST":
		print("Posting data")
		print(request.POST)
		print(request.FILES)
		return JsonResponse({'status' : True })


def SignIn(request):
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title" : "Health Provider Login",
			"route" : "/healthprovider",
			"color" : "primary"
			})
	elif request.method == "POST":
		if signin("healthprovider", request):
			return redirect('healthprovider:dashboard')
		return redirect('healthprovider:signin')


# @match_role("healthprovider")
def Dashboard(request):
	return render(request, 'healthprovider/dashboard/base.html.j2', context={
		"title" : "Dashboard",
		"user" : "User"
		})

def BasicDetails(request):
	return render(request, 'healthprovider/dashboard/basic_details.html.j2', context={
		"title" : "Basic Details",
		"section" : "Basic Details",
		})

def ContactDetails(request):
	return render(request, 'healthprovider/dashboard/contact_details.html.j2', context={
		"title" : "Contact Details",
		"section" : "Contact Details",
		})

def Branches(request):
	return render(request, 'healthprovider/dashboard/branches.html.j2', context={
		"title" : "Branches",
		"section" : "Branches",
		})

def Specialities(request):
	return render(request, 'healthprovider/dashboard/specialities.html.j2', context={
		"title" : "Specialities",
		"section" : "Specialities",
		})


def Facilities(request):
	return render(request, 'healthprovider/dashboard/facilities.html.j2', context={
		"title" : "Facilities",
		"section" : "Facilities",
		})

def Offerings(request):
	return render(request, 'healthprovider/dashboard/offerings.html.j2', context={
		"title" : "Offerings",
		"section" : "Offerings",
		})

def SpecialHealthChecks(request):
	return render(request, 'healthprovider/dashboard/special_health_checks.html.j2', context={
		"title" : "Special Health Checks",
		"section" : "Special Health Checks",
		})

def Plans(request):
	return render(request, 'healthprovider/dashboard/plans.html.j2', context={
		"title" : "Plans",
		"section" : "Plans",
		})
