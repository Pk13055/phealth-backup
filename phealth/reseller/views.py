from django.shortcuts import render
from phealth.utils import signin

# Create your views here.


def SignIn(request):
	'''
		signin route for the reseller

	'''
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Reseller Login",
			"route": "/reseller",
			"color": "success"
		})
	elif request.method == "POST":
		if signin("reseller", request):
			return redirect('sponsor:dashboard_home')
		return redirect('sponsor:signin')
