import datetime
import hashlib
from random import randint

import dateutil
import requests
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer

from api.models import (Address, Appointment, Clinician, Coupon, Provider,
                        Speciality, User)
from phealth import utils
from phealth.utils import match_role

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
	return render(request, 'index.html', context={
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


@csrf_exempt
@match_role(["clinician", "healthprovider", "poc"])
def appointment_list(request):
	''' route to retrieve appointment data | start and end as get params '''

	status = 1
	get_time = lambda x: dateutil.parser.parse(x)
	init_set = Appointment.objects

	# filter initial appointment set according to user type
	u = User.objects.filter(email=request.session['email']).first()
	if u.role == "clinician":
		c = Clinician.objects.filter(user=u).first()
		init_set = c.appointment_set
	elif u.role == "healthprovider":
		p = Provider.objects.filter(poc=u).first()
		init_set = p.appointment_set
	elif u.role == "poc":
		# handle POC differently
		pass


	if request.method == "GET":
		from_date = request.GET.get('start', False)
		to_date = request.GET.get('end', False)
	elif request.method == "POST":
		from_date = request.POST.get('start', False)
		to_date = request.POST.get('end', False)

	if not from_date and not to_date:
		status = 0
		return JsonResponse([], safe=False)

	from_date = get_time(from_date)
	to_date = get_time(to_date)

	class AppointmentSerializer(ModelSerializer):
		title = serializers.CharField(source='status')
		start = serializers.DateTimeField(source='from_timestamp')
		end = serializers.DateTimeField(source='to_timestamp')
		className = serializers.CharField(source='css_class')
		# add additional information here later
		class Meta:
			model = Appointment
			fields = ('id', 'start', 'end', 'title', 'className')

	q = init_set.filter(from_timestamp__gte=from_date, to_timestamp__lte=to_date)
	id = request.GET.get('id', False) or request.POST.get('id', False)
	if u.role == "healthprovider" and id and id != '':
		q = q.filter(under_id=id)

	data = AppointmentSerializer(q, many=True)

	return JsonResponse(data.data, safe=False)
