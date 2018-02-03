from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.


def SignUp(request):
	if request.method == "GET":
		return render(request, 'sponsor/registration.html.j2', context={
			'route': "/sponsor"
		})
	elif request.method == "POST":
		print("Posting data")
		print(request.POST)
		print(request.FILES)
		return JsonResponse({'status' : True })


def SignIn(request):
	return render(request, 'common/signin.html.j2', context={
		"title" : "Sponsor Login",
		"route" : "/sponsor",
		"color" : "warning"
		})
