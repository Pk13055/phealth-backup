from django.shortcuts import render

# Create your views here.


def SignUp(request):
	if request.method == "GET":
		return render(request, 'clinician/registration.html.j2', context={'route': "/clinician"})
	elif request.method == "POST":
		print("Posting data")
		print(request.POST)
		print(request.FILES)
		return JsonResponse({'status' : True })


def SignIn(request):
	return render(request, 'common/signin.html.j2', context={
		"title": "Clinician Login",
		"route": "/clinician",
		"color": "info"
	})


def calender(request):
	''' handles the calender page for clincian timings
	and bookings
	'''
	return render(request, 'clinician/calender.html.j2', context={
		'title' : "Set your timings"
		})
