import datetime
import hashlib
from random import randint

import requests
from django.contrib.auth.hashers import check_password, make_password
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from ipware import get_client_ip

from api.models import *

# contains all the comon code for utility purposes

def get_sponsor(email):
	sponsor = Sponsor.objects.filter(user__email=email).first()
	return sponsor

def get_clinician(email):
	clinician = Clinician.objects.filter(user__email=email).first()
	return clinician

def get_provider(email):
	provider = Provider.objects.filter(poc__email=email).first()
	return provider

def match_role(role_type):
	'''
		decorator that wraps protected views
	 	retriving role from session
	'''
	if not isinstance(role_type, list): role_type = [role_type]
	def inner_decorator(function):
		def wrapper(request, *args, **kwargs):
			if 'role' in request.session and request.session['role'] in role_type:
				return function(request, *args, **kwargs)
			else:
				return redirect('/' + request.path_info.split('/')[1] + '/signin')
		return wrapper
	return inner_decorator


def getIP(request):
	''' returns the client IP
		based on the request object
	'''
	client_ip, is_routable = get_client_ip(request)
	# is_routable = True, False, None
	return client_ip, is_routable

def signin(role, request):
	''' signin middleware
	'''
	email = request.POST['username']
	password = request.POST['password']
	print(password)

	# implemented type should only support list
	if not isinstance(role, (list, str,)):
		raise Http404("Signin functionality for type not implemented")

	if not isinstance(role, list): role = [role]

	u = User.objects.filter(email=email).first()

	client_ip, is_routable = getIP(request)
	if client_ip is not None: u.last_IP = client_ip
	status = False

	if u and check_password(password, u.password) and (u.role in role or role in u.role):
		u.last_update=datetime.datetime.now()
		request.session['email'] = email
		request.session['role'] = u.role
		request.session['pk'] = u.pk
		status = True

	u.save()
	return status

def generate_payment_data(request, to, amount, product_info, test=False):
	PAYU_BASE_URL = 'https://secure.payu.in/_payment'
	MERCHANT_KEY = 'omKM0P'
	SALT = 'Rf0OQdPE'

	# email = request.session['email']
	# u = Users.objects.get(email=email)
	u = True

	if u:
		hash_object = hashlib.sha256(b'randint(0,20)')
		hash_string = ''

		data = {
			'key': MERCHANT_KEY,
			'txnid': hash_object.hexdigest()[0:20],
			'amount': str(amount),
			'productinfo': product_info,
			# 'firstname': u.firstname,
			# 'email': u.email,
			# 'phone': u.phone,
			'firstname': 'Test',
			'email': 'test@test.in',
			'phone': '1010101010',
			'surl': reverse('common:payment_success'),
			'furl': reverse('common:payment_failure'),
		}

		hash_sequence = [
			'key', 'txnid', 'amount', 'productinfo', 'firstname', 'email', 'udf1',
			'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8', 'udf9', 'udf10'
		]

		hash_string = '|'.join([str(data[_]) if _ in data else '' for _ in hash_sequence ]) + '|' + SALT
		data['hash'] = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

		return PAYU_BASE_URL, data

	return None

def perdelta(start, end, delta):
	'''
		function that generates a list of date/time/datetime
	'''
	t = 'datetime'
	if isinstance(start, datetime.time):
		start = datetime.datetime.combine(datetime.datetime.now().date(), start)
		end = datetime.datetime.combine(datetime.datetime.now().date(), end)
		t = 'time'
	elif isinstance(start, datetime.date):
		start = datetime.datetime.combine(start, datetime.datetime.now().time())
		end = datetime.datetime.combine(end, datetime.datetime.now().time())
		t = 'date'
	curr = start
	timings = []
	while curr <= end:
		timings.append(curr.time() if t == 'time' else curr.date() if t == 'date' else curr)
		curr += delta
	return timings
