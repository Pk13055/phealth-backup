from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def logout(request):
	''' ajax request to this view to logout
	'''
	if request.method == "POST":
		if 'role' in request.session:
			del request.session['role']
			del request.session['email']
			return JsonResponse({'status' : True })
	return JsonResponse({ 'status' : False })
