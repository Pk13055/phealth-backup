from django.http import JsonResponse

# contains all the comon code for authentication purposes


def match_role(role_type):
	'''
		decorator that wraps protected views
	 	retriving role from session
	'''
	def inner_decorator(function):
		def wrapper(request, *args, **kwargs):
			print(request.session)
			if 'role' in request.session and role_type in request.session['role']:
				return function(request, *args, **kwargs)
			else:
				return JsonResponse({ 'status' : "Login first" })
		return wrapper
	return inner_decorator
