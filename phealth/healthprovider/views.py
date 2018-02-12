from django.shortcuts import render
from phealth.utils import match_role, signin, redirect
from django.http import JsonResponse
from django import forms
from api.models import Healthproviders, Users, HealthprovidersSpeciality, Availablefacilities
# Create your views here.


def SignUp(request):
	if request.method == "GET":
		return render(request, 'healthprovider/registration.html.j2', context={ 'route': "/healthprovider" })
	elif request.method == "POST":
		print("Posting data")
		print(request.POST)
		print(request.FILES)
		return JsonResponse({'status' : True })


def SignIn(request):
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title" : "Health Provider Login",
			"route" : "/healthprovider",
			"color" : "primary"
			})
	elif request.method == "POST":
		if signin("healthprovider", request):
			return redirect('healthprovider:dashboard_home')
		return redirect('healthprovider:signin')

@match_role("healthprovider")
def dashboard(request):
	''' route for dashboard home '''

	u = Healthproviders.objects.filter(users__email=request.session['email']).first()

	class BasicForm(forms.ModelForm):

		class Meta:
			model = Healthproviders
			fields = ('__all__')

	if request.method == "POST":
		b = BasicForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()
		print(b)

	return render(request, 'healthprovider/dashboard/home.html.j2', context={
		"title": "Dashboard Home",
		"form_title" : "Edit Basic Information",
		"form" : BasicForm(instance=u)
	})

@match_role("healthprovider")
def contact_details(request):
	''' route for dashboard contact details '''

	u = Healthproviders.objects.filter(users__email=request.session['email']).first()

	class BasicForm(forms.ModelForm):

		class Meta:
			model = Users
			fields = ('mobile', 'email', 'firstname', 'middlename', 'lastname')

	if request.method == "POST":
		b = BasicForm(request.POST, request.FILES, instance=u.users)
		if b.is_valid():
			b.save()
		print(b)

	return render(request, 'healthprovider/dashboard/home.html.j2', context={
		"title": "Contact Details Dashboard",
		"form_title" : "Edit Contact Information",
		"form" : BasicForm(instance=u.users)
	})

# def branches(request):
# 	return render(request, 'healthprovider/dashboard/branches.html.j2', context={
# 		"title" : "Branches",
# 		"section" : "Branches",
# 		})

def specialities(request):
	''' route for dashboard specialities '''

	u = Healthproviders.objects.filter(users__email=request.session['email']).first()

	class SpecialityForm(forms.ModelForm):
		class Meta:
			model = HealthprovidersSpeciality
			fields = ('__all__')
			widgets = {
				'validity' : forms.TextInput(attrs={
					'placeholder' : "YYYY-MM-DD"
				})
			}

	EditFormSet = forms.modelformset_factory(HealthprovidersSpeciality, fields=('__all__'), extra=0)

	if request.method == "POST":
		_forms = []
		if request.POST['data_type'] == "add":
			c = SpecialityForm(request.POST, request.FILES)
			_forms.append(c)
		elif request.POST['data_type'] == "update":
			c = EditFormSet(request.POST, request.FILES)
			_forms += c.forms

		for form in _forms:
			if form.is_valid():
				d = form.save(commit=False)
				d.healthproviders = u
				d.save()
			else:
				print("errors :", form.errors)


	edit_forms = EditFormSet(queryset=HealthprovidersSpeciality.objects.filter(healthproviders__healthproviders_id=u.healthproviders_id))
	return render(request, 'healthprovider/dashboard/speciality.html.j2', context={
		"title": "Specialities Dashboard",
		"form" : SpecialityForm(),
		"edit_forms": edit_forms
	})


def facilities(request):
	''' route for dashboard facilities '''

	u = Healthproviders.objects.filter(users__email=request.session['email']).first()

	class FacilityForm(forms.ModelForm):
		class Meta:
			model = Availablefacilities
			fields = ('facilities_services', 'facilities')
			widgets = {
				'validity' : forms.TextInput(attrs={
					'placeholder' : "YYYY-MM-DD"
				})
			}

	EditFormSet = forms.modelformset_factory(Availablefacilities, fields=('facilities_services', 'facilities'), extra=0)

	if request.method == "POST":
		_forms = []
		if request.POST['data_type'] == "add":
			c = FacilityForm(request.POST, request.FILES)
			_forms.append(c)
		elif request.POST['data_type'] == "update":
			c = EditFormSet(request.POST, request.FILES)
			_forms += c.forms

		for form in _forms:
			if form.is_valid():
				d = form.save(commit=False)
				d.healthproviders = u
				d.save()
			else:
				print("errors :", form.errors)


	edit_forms = EditFormSet(queryset=Availablefacilities.objects.filter(healthproviders__healthproviders_id=u.healthproviders_id))
	return render(request, 'healthprovider/dashboard/facility.html.j2', context={
		"title": "Facilities Dashboard",
		"form" : FacilityForm(),
		"edit_forms": edit_forms
	})

# def offerings(request):
# 	return render(request, 'healthprovider/dashboard/offerings.html.j2', context={
# 		"title" : "Offerings",
# 		"section" : "Offerings",
# 		})

# def special_health_checks(request):
# 	return render(request, 'healthprovider/dashboard/special_health_checks.html.j2', context={
# 		"title" : "Special Health Checks",
# 		"section" : "Special Health Checks",
# 		})

# def plans(request):
# 	return render(request, 'healthprovider/dashboard/plans.html.j2', context={
# 		"title" : "Plans",
# 		"section" : "Plans",
# 		})

def doctors_list(request):
	''' route for dahsboard doctors list '''

	return render(request, 'healthprovider/dashboard/doctors_list.html.j2', context={
		"title": "Doctors Appointment List",
	})
