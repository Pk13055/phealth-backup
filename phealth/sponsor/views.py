from django.shortcuts import render, redirect
from django.http import JsonResponse
from phealth.utils import match_role, signin
from django import forms
# from api.models import Sponsors, Coupons
# Create your views here.

# sponsor common routes


def SignUp(request):
	if request.method == "GET":
		return render(request, 'sponsor/registration.html.j2', context={
			'route': "/sponsor"
		})
	elif request.method == "POST":
		print("Posting data")
		print(request.POST)
		print(request.FILES)
		return JsonResponse({'status': True})


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

	u = Sponsors.objects.filter(users__email=request.session['email']).first()

	class SponsorForm(forms.ModelForm):

		class Meta:
			model = Sponsors
			exclude = ('users', 'image', 'activefrom', 'activeto',)


	if request.method == "POST":
		b = SponsorForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()

	return render(request, 'sponsor/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit basic information",
		"form" : SponsorForm(instance=u)
	})


# @match_role("sponsor")
# def participants(request):
# 	''' route for dashboard participants'''
# 	if request.method == "POST":
# 		pass
# 		# handle the form parsing and data etc here

# 	return render(request, 'sponsor/dashboard/participants.html.j2', context={
# 		"title": "Dashboard - participants details "
# 	})


@match_role("sponsor")
def discounts(request):
	''' route for dashboard discounts '''

	u = Sponsors.objects.filter(users__email=request.session['email']).first()

	class DiscountForm(forms.ModelForm):
		class Meta:
			model = Coupons
			exclude = ('applicablesponsor', 'uniquecode',)
			widgets = {
				'validity' : forms.TextInput(attrs={
					'placeholder' : "YYYY-MM-DD"
					})
			}

	EditFormSet = forms.modelformset_factory(Coupons, exclude=('applicablesponsor',
		'uniquecode',), extra=0)

	if request.method == "POST":
		_forms = []
		if request.POST['data_type'] == "add":
			c = DiscountForm(request.POST, request.FILES)
			_forms.append(c)
		elif request.POST['data_type'] == "update":
			c = EditFormSet(request.POST, request.FILES)
			_forms += c.forms

		for form in _forms:
			if form.is_valid():
				d = form.save(commit=False)
				d.applicablesponsor = u.users.users_id
				d.save()
			else:
				print("errors :", form.errors)


	edit_forms = EditFormSet(queryset=Coupons.objects.filter(applicablesponsor=u.users.users_id))
	return render(request, 'sponsor/dashboard/discounts.html.j2', context={
		"title": "Dashboard - discounts details",
		"form" : DiscountForm(),
		"edit_forms": edit_forms
	})
