import datetime
import hashlib
from random import randint

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.context_processors import csrf
from phealth import utils
from api.models import User
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
import requests

# Create your views here.

@csrf_exempt
def logout(request):
	''' ajax request to this view to logout
	'''
	if 'role' in request.session:
		request.session.pop('role')
		request.session.pop('email')
	return redirect('/')

def home_route(request):
	'''site home route for debugging purposes'''
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

@require_POST
def send_OTP(request):
	''' takes a given OTP value from the
	session and sends to a specified mobile number
	and email
	'''
	print("POST DATA", request.POST)
	try:
		mobile = request.POST['mobile']
		email = request.POST['email']
		otp = request.session['otp']
	except:
		return JsonResponse({ 'status' : "Invalid Request" })

	# # Email sending
	# try:
	# 	email = send_mail("Registration OTP", "Code: %d" % otp, "rajesh@mbrinformatics.com", [email],
	# 		fail_silently=False)
	# except Exception as e:
	# 	return JsonResponse({ 'status' : "E-mail failed to send | %s" % str(e) })

	# Mobile OTP sending
	base_url = "http://api.msg91.com/api/sendhttp.php"
	params = {
		'sender' : "CLICKHEALTH",
		'route' : 4,
		'country' : 91,
		'mobiles' : [ mobile ],
		'authkey' : '182461AjomJGPHB5a0041cb',
		'message' : "Verification OTP : %d" % otp
	}
	try:
		r = requests.get(base_url, params=params)
		if r.status_code != 200:
			raise Exception("Invalid params")
	except Exception as e:
		return JsonResponse({ 'status' : "SMS failed to send | %s" % str(e) })

	return JsonResponse({ 'status' : "OTP sent successfully!" })
