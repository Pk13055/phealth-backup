from django.shortcuts import render
from django.http import JsonResponse
from phealth.utils import match_role
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
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title" : "Sponsor Login",
			"route" : "/sponsor",
			"color" : "warning"
			})
	elif request.method == "POST":
		if signin("sponsor", request):
			return redirect('sponsor:dashboard')
		return redirect('sponsor:signin')


@match_role("sponsor")
def dashboard(request):
	return JsonResponse({'status' : True })
