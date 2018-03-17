import datetime
import hashlib
from random import randint
import requests

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.context_processors import csrf
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from rest_framework.serializers import ModelSerializer
from rest_framework.renderers import JSONRenderer
from api.models import User, Speciality, Address, Coupon
from phealth import utils

# Create your views here.

@csrf_exempt
def logout(request):
	''' ajax request to this view to logout
	'''
	if 'role' in request.session:
		request.session.pop('role')
		request.session.pop('email')
	return redirect('home')

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
@csrf_exempt
def send_OTP(request, gen=False):
	''' takes a given OTP value from the
	session and sends to a specified mobile number
	and email
	'''
	print("POST DATA", request.POST)
	try:
		mobile = request.POST['mobile']
		email = request.POST['email']
		if 'generate' in request.POST or gen:
			otp = randint(1, 99999)
			request.session['otp'] = otp
		else:
			otp = request.session['otp']
	except:
		return JsonResponse({
			'status' : False,
			'data' : ["Invalid Request"]
			})

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
		return JsonResponse({
			'status' : False,
			'data' : ["SMS failed to send | %s" % str(e)]
			})

	return JsonResponse({
		'status' : True,
		'data' : [str(otp)]
		})


@require_POST
@csrf_exempt
def autocomplete(request, category, query):
	''' route takes partial string and returns
		relevant data
	'''
	final_data = None
	queryset = None
	if category == 'condition':
		queryset = Speciality.objects.filter(name__icontains=query).all()
		if queryset:
			model_type = Speciality
	elif category == 'location' or category == 'city':
		queryset = Address.objects.filter(Q(extra__icontains=query) |
			Q(city__name__icontains=query) | Q(city__state__name__icontains=query)).all()
		if queryset:
			model_type = Address

	if queryset:
		class DataSerializer(ModelSerializer):
			class Meta:
				model = model_type
				depth = 5
				fields = '__all__'
		data = DataSerializer(queryset, many=True)
		# final_data = JSONRenderer().render(data.data).decode()
		final_data = data.data
		return JsonResponse({
			'status' : True,
			'data' : final_data,
			})

	return JsonResponse({
		'status' : False,
		'data' : [],
		})

@require_POST
@csrf_exempt
def verify_coupon(request):
	status = False
	data = {}
	if 'coupon' in request.POST:
		code = request.POST['coupon']
		c = Coupon.objects.filter(name=str(code)).first()
		if c and c.validity and c.expiry > datetime.datetime.now().date()\
		 and c.quantity and 'coupon' not in request.session:
			request.session['coupon'] = c.id
			data['type'] = c.type
			data['amount'] = c.amount
			status = True
	else:
		status = False
	return JsonResponse({
		'status' : status,
		'data' : data
		})
