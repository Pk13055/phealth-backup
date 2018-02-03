from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
import requests
from random import randint
# Create your views here.


def otphandle(request):
	''' @param mobile number
		@param email
		@return success
	'''
	if request.method == "GET":
		print("GET REQUEST FOR VERIFICATION")
		return JsonResponse({ 'status' : "Invalid Request type" })

	elif request.method == "POST":

		# if 'otp' in request.COOKIES:
		# 	return JsonResponse({ 'status' : "Already sent" })

		otp = randint(10000, 999999)
		request.COOKIES['otp'] = otp

		mobile = request.POST.get('mobile')
		email = request.POST.get('email')

		message = ("Greetings!\n Your OTP for "
			"registration is : %d") % otp

		try:
			email = EmailMessage('Subject', message, to=[email])
			email.send()
		except:
			resp =  JsonResponse({ 'status' : False })
			return resp

		API_DATA = {
			'authkey': '182461AjomJGPHB5a0041cb',
		 	'country': '91',
		 	'message': message,
		 	'mobiles': str(mobile),
		 	'route': '4',
		 	'sender': 'PHEALT'
	 	}
		resp = requests.get("http://api.msg91.com/api/sendhttp.php?", params=API_DATA)
		if resp.status_code == 200:
			resp =  JsonResponse({ 'status' : True })
			resp.set_cookie('otp', otp)
		else:
			resp =  JsonResponse({ 'status' : False })

		return resp


