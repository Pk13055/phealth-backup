from django.shortcuts import render, redirect
from phealth.utils import signin, match_role

# Create your views here.


def SignIn(request):

	'''
		signin route for the sales agent

	'''
	if request.method == "GET":
		return render(request, 'site_admin/signin.html', context={
			"title": "Administrator Login",
			"route": "/site_admin",
			"color": "default"
		})
	elif request.method == "POST":
		print(request.POST)
		if signin("admin", request):
			return redirect('site_admin:dashboard_home')
		return redirect('site_admin:signin')


def SignUp(request):
	return redirect('site_admin:dashboard_home')

# Main dashboard routes

@match_role("admin")
def dashboard(request):
	''' main dashboard route
	'''
	return render(request, 'site_admin/dashboard/home.html.j2', context={
			'title' : "Basic Details",
		})

@match_role("admin")
def cms(request):
	''' main CMS route for the admin
	'''
	return render(request, 'site_admin/dashboard/cms.html.j2', context={
			'title' : "CMS Filler",
		})


@match_role("admin")
def tokens(request):
	''' route for super admin access
	'''
	return redirect('/admin/')
