import datetime
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from api.models import *
from ipware import get_client_ip


# contains all the comon code for utility purposes


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
	u = Users.objects.get(email=email)

	client_ip, is_routable = getIP(request)
	if client_ip is not None:
		u.update(last_IP=clien_ip)

	if u and check_password(password, u.password) and (u.role in role or role in u.role):
		u.update(last_update = datetime.datetime.now())
		request.session['email'] = email
		request.session['role'] = u.role
		return True
	return False
