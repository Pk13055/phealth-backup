from django.shortcuts import render, redirect
from phealth.utils import signin, match_role

# Create your views here.


def SignIn(request):
	'''
		signin route for the reseller

	'''
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Reseller Login",
			"route": "/reseller",
			"color": "danger"
		})
	elif request.method == "POST":
		if signin("reseller", request):
			return redirect('reseller:dashboard_home')
		return redirect('reseller:signin')


def SignUp(request):
	''' signup route for the reseller
	'''
	return redirect('reseller:dashboard_home')

# Main dashboard routes

@match_role("reseller")
def dashboard(request):
	''' main dashboard route
	'''
	return render(request, 'reseller/dashboard/home.html.j2', context={
			'title' : "Basic Details"
		})

@match_role("reseller")
def discounts(request):
	''' route for discount card handling
	'''
	return render(request, 'reseller/dashboard/discounts.html.j2', context={
			'title' : "Discount Cards",
		})
