from django.shortcuts import render

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
	return render(request, 'common/signin.html.j2', context={
		"title" : "Health Provider Login",
		"route" : "/healthprovider",
		"color" : "primary"
		})
