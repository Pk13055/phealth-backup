from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from django import forms
from phealth.utils import getIP
from api.models import User, Sponsor
import random

# Create your views here.

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('__all__')
		# exclude = ()

# sponsor common routes
def SignUp(request):

	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsor
			exclude = ('user',)

	if request.method == "POST":
		print(request.POST, request.FILES)
		s = SponsorForm(request.POST, request.FILES)
		u = UserForm(request.POST, request.FILES)
		print(s.is_valid(), u.is_valid())
		print(request.session['otp'], request.POST['otp'])
		if s.is_valid() and u.is_valid() and \
			str(request.POST['otp']) == str(request.session['otp']):
			user = u.save(commit=False)
			ip_addr, del_val = getIP(request)
			if ip_addr: user.last_IP = ip_addr
			user.role = 'sponsor'
			user.save()
			sponsor = s.save(commit=False)
			sponsor.user = user
			sponsor.save()
			del request.session['otp']
			return redirect('sponsor:signin')
		user_form = u
		sponsor_form = s
		errors = [u.errors, s.errors, "OTP did not match!"]
		print(errors)

	elif request.method == "GET":
		user_form = UserForm()
		sponsor_form = SponsorForm()
		errors = None

	if 'otp' not in request.session:
		request.session['otp'] = random.randint(1, 9999)

	return render(request, 'sponsor/registration.html.j2', context={
		'title' : "Sponsor Registration",
		'route': "/sponsor",
		'user_form' : user_form,
		'sponsor_form' : sponsor_form,
		'errors' : errors
	})

def SignIn(request):
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Sponsor Login",
			"route": "/sponsor",
			"color": "warning"
		})
	elif request.method == "POST":
		if signin("sponsor", request):
			return redirect('sponsor:dashboard_home')
		return redirect('sponsor:signin')


# Dashboard routes

@match_role("sponsor")
def dashboard(request):
	''' route for dashboard home '''

	u = Sponsor.objects.filter(user__email=request.session['email']).first()

	return render(request, 'sponsor/dashboard/basic_details.html.j2', context={
		"title": "Basic details",
	})


@match_role("sponsor")
def discounts(request):
	''' route for dashboard discounts '''

	u = Sponsor.objects.filter(user__email=request.session['email']).first()

	return render(request, 'sponsor/dashboard/discountcards.html.j2', context={
		'title' : "Discount cards",
		})


@match_role("sponsor")
def user_view(request):
	''' route for adding and viewing users '''

	u = Sponsor.objects.filter(user__email=request.session['email']).first()

	return render(request, 'sponsor/dashboard/users.html.j2', context={
		'title' : "User Base",
		})
