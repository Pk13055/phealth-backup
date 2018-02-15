from django.shortcuts import render

# Create your views here.


def SignIn(request):
	'''
		signin route for the sales agent

	'''
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Reseller Login",
			"route": "/reseller",
			"color": "success"
		})
	elif request.method == "POST":
		if signin("reseller", request):
			return redirect('salesagent:dashboard_home')
		return redirect('salesagent:signin')
