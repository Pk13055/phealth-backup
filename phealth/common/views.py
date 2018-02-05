from django.shortcuts import render
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
		return JsonResponse({'status' : True })
	return JsonResponse({ 'status' : False })
