from django.shortcuts import render
from phealth.utils import signin, match_role
# Create your views here.


def SignIn(request):
	'''
		signin route for the sales agent

	'''
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Sales Agent Login",
			"route": "/salesagent",
			"color": "warning"
		})
	elif request.method == "POST":
		if signin("salesagent", request):
			return redirect('salesagent:dashboard_home')
		return redirect('salesagent:signin')


def SignUp(request):
	''' signup route for salesagent '''
	return render(request, 'salesagent/signup.html.j2', context={
			'title' : "Salesagent - Signup"
		})

# Main dashboard routes

@match_role("salesagent")
def dashboard(request):
	''' main dashboard route
	'''
	return render(request, 'salesagent/dashboard/home.html.j2', context={
			'title' : "Basic Details"
		})

@match_role("salesagent")
def reseller_register(request):
	''' route for reseller registration '''
	return render (request, 'salesagent/dashboard/reseller.html.j2', context={
			'title' : "Reseller Registration",
		})


@match_role("salesagent")
def discounts(request):
	''' route for discount card purchase '''
	return render(request, 'salesagent/dashboard/discounts.html.j2', context={
			'title' : "Discount cards",
		})
