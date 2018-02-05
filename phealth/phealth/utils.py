from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from api.models import *

# contains all the comon code for authentication purposes


def match_role(role_type):
	'''
		decorator that wraps protected views
	 	retriving role from session
	'''
	def inner_decorator(function):
		def wrapper(request, *args, **kwargs):
			if 'role' in request.session and role_type in request.session['role']:
				return function(request, *args, **kwargs)
			else:
				return JsonResponse({ 'status' : "Login first" })
		return wrapper
	return inner_decorator


def signin(role, request):
	email = request.POST['username']
	password = request.POST['password']
	u = Users.objects.filter(email=email).first()
	if u and check_password(password, u.enc_password) and u.role.role == role:
		request.session['email'] = email
		if 'role' in request.session:
			if not isinstance(request.session['role'], list):
				request.session['role'] = [request.session['role']]
			request.session['role'].append(role)
		else:
			request.session['role'] = [role]
		return True
	return False