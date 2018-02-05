from django.shortcuts import render
from phealth.utils import match_role
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


@match_role("healthprovider")
def dashboard(request):
	return JsonResponse({'status' : True })
