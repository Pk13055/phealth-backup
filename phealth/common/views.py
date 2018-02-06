from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def logout(request):
	''' ajax request to this view to logout
	'''
	if 'role' in request.session:
		request.session.pop('role')
		request.session.pop('email')
	return redirect('/')

# site home route
def home_route(request):
	return render(request, 'home.html.j2', context={
		'title' : "HOME"
		})

