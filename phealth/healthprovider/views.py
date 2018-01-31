from django.shortcuts import render

# Create your views here.

def SignUp(request):
    return render(request, 'healthprovider/registration.html.j2', context={
    	'route' : "/healthprovider"
    	})


def SignIn(request):
	return render(request, 'common/signin.html.j2', context={
		"title" : "Health Provider Login",
		"route" : "/healthprovider",
		"color" : "primary"
		})
