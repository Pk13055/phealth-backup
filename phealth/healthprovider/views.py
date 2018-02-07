from django.shortcuts import render
from phealth.utils import match_role
from django.http import JsonResponse
from django import forms
from api.models import Healthproviders
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

@match_role("sponsor")
def dashboard(request):
	''' route for dashboard home '''

	u = Healthproviders.objects.filter(users__email=request.session['email']).first()

	class BasicForm(forms.ModelForm):

		class Meta:
			model = Healthproviders
			fields = ('__all__')

	if request.method == "POST":
		b = BasicForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()
		print(b)

	return render(request, 'healthprovider/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit Basic Information",
		"form" : BasicForm(instance=u)
	})

def contact_details(request):
	return render(request, 'healthprovider/dashboard/contact_details.html.j2', context={
		"title" : "Contact Details",
		"section" : "Contact Details",
		})

def branches(request):
	return render(request, 'healthprovider/dashboard/branches.html.j2', context={
		"title" : "Branches",
		"section" : "Branches",
		})

def specialities(request):
	return render(request, 'healthprovider/dashboard/specialities.html.j2', context={
		"title" : "Specialities",
		"section" : "Specialities",
		})


def facilities(request):
	return render(request, 'healthprovider/dashboard/facilities.html.j2', context={
		"title" : "Facilities",
		"section" : "Facilities",
		})

def offerings(request):
	return render(request, 'healthprovider/dashboard/offerings.html.j2', context={
		"title" : "Offerings",
		"section" : "Offerings",
		})

def special_health_checks(request):
	return render(request, 'healthprovider/dashboard/special_health_checks.html.j2', context={
		"title" : "Special Health Checks",
		"section" : "Special Health Checks",
		})

def plans(request):
	return render(request, 'healthprovider/dashboard/plans.html.j2', context={
		"title" : "Plans",
		"section" : "Plans",
		})
