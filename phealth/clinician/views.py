from django.shortcuts import render

# Create your views here.

def SignUp(request):
    return render(request, 'clinician/registration.html.j2', context={
    	'route' : "/clinician"
    	})


def SignIn(request):
	return render(request, 'common/signin.html.j2', context={
		"title" : "Clinician Login",
		"route" : "/clinician",
		"color" : "info"
		})
