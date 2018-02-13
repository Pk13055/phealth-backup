import datetime
import hashlib
from random import randint

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.context_processors import csrf
from phealth import utils
from api.models import User

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

# payment routes
def payment_success(request):
	return JsonResponse({"status": True})

def payment_failure(request):
	return JsonResponse({"status": False})

def payment_init(request):
	action, data = utils.generate_payment_data(request, 'user', 123.45, 'test')

	if data:
		return render(request, 'common/payment/init.html.j2', context={
			'title': 'Payment',
			'action': action,
			'data': data
		})