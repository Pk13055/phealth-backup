from django.shortcuts import render

# Create your views here.

def SignUp(request):
    return render(request, 'sponsor/registration.html.j2', context={
    	'route' : "/sponsor"
    	})

def SignIn(request):
	return render(request, 'common/signin.html.j2', context={
		"title" : "Sponsor Login",
		"route" : "/sponsor",
		"color" : "warning"
		})
