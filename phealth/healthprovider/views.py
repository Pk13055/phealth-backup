import datetime
import json
import random
from random import randint
import requests
from datatableview import (Datatable, DateTimeColumn, TextColumn,
                           ValuesDatatable)
from datatableview.helpers import make_xeditable
from datatableview.views import DatatableView, XEditableDatatableView
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.validators import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from querystring_parser import parser
from rest_framework.serializers import ModelSerializer

from api.models import (Appointment, Clinician, Location, Organization,
                        Provider, Speciality, Transaction, User,Amenity)
from phealth.utils import get_provider, match_role, redirect, signin

# Create your views here.

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('__all__')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile', 'password',)

    widgets = {
        'password': forms.PasswordInput()
    }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

class ProviderregForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ('service_type', 'name',)

    def __init__(self, *args, **kwargs):
        super(ProviderregForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ('service_name', 'service_image',)

    def __init__(self, *args, **kwargs):
        super(AmenityForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


def SignUp(request):



    if request.method == 'POST':
        uform = UserForm(request.POST)
        if uform.is_valid():

            #otp here
            mobile = request.POST['mobile']
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['username'] = request.POST['email']
            request.POST._mutable = mutable

            request.session['userdata'] = request.POST
            otp = randint(1, 99999)
            request.session['otp'] = otp
            base_url = "http://api.msg91.com/api/sendhttp.php"
            params = {
                'sender': "CLICKH",
                'route': 4,
                'country': 91,
                'mobiles': [mobile],
                'authkey': '182461AjomJGPHB5a0041cb',
                'message': "Verification OTP : %d" % otp
            }
            r = requests.get(base_url, params=params)


            return redirect('healthprovider:otp')
    else:
        uform = UserForm()
        prform = ProviderregForm()
    return render(request, 'healthprovider/registration.html.j2', context={
        "uform": uform, "prform":prform,
    })


def otp(request):
	if request.method == "POST":
		if (int(request.POST['otp']) == int(request.session['otp'])):
			request.POST = request.session['userdata']
			uform = UserForm(request.POST)
			prform = ProviderregForm(request.POST)
			prpost = prform.save(commit=False)
			upost = uform.save(commit=False)
			upost.role = "healthprovider"
			upost.password = make_password(request.POST['password'])
			upost.save()
			prpost.poc = User.objects.get(pk=upost.pk)
			prpost.save()
			return redirect('healthprovider:signin')

		else:
			return render(request, 'healthseeker/registration/otp.html', {'error': "Invalid Otp"})

	else:
		return render(request, 'healthseeker/registration/otp.html', {})




def SignIn(request):
    if request.method == "GET":
        return render(request, 'common/signin.html.j2', context={
            "title" : "Healthprovider Login",
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

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    if request.method == "POST":
        u = UserForm(request.POST, request.FILES, instance=p.poc)
        if u.is_valid():
            u.save()
        print(u)

    return render(request, 'healthprovider/dashboard/home.html.j2', context={
        "title": "Home",
        "form_title" : "Edit Basic Information",
        "form" : UserForm(instance=p.poc)
    })

@match_role("healthprovider")
def branches(request):
    ''' route for provider branches '''

    return JsonResponse({"status": True})

@match_role("healthprovider")
def specialities(request):
    ''' route for provider specialities '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    class SpecialityForm(forms.ModelForm):
        class Meta:
            model = Speciality
            fields = ('__all__')

    class ProviderForm(forms.ModelForm):
        class Meta:
            model = Provider
            fields = ('specialities',)

        def __init__(self, *args, **kwargs):
            super(ProviderForm, self).__init__(*args, **kwargs)
            self.fields['specialities'].widget = forms.CheckboxSelectMultiple()
            self.fields['specialities'].queryset = Speciality.objects.all()

    edit_form = ProviderForm(instance=p)

    if request.method == "POST":
        if request.POST['type'] == 'add':
            s = SpecialityForm(request.POST, request.FILES).save(commit=False)
            s.save()
            p.specialities.add(s)

        if request.POST['type'] == 'edit':
            h = ProviderForm(request.POST, request.FILES, instance=p)
            if h.is_valid():
                h.save()
            else:
                errors += [h.errors]
            edit_form = h

    return render(request, 'healthprovider/dashboard/speciality.html.j2', context={
        "title": "Specialities",
        "form" : SpecialityForm(),
        "edit_form": edit_form,
    })

@match_role("healthprovider")
def clinicians(request):
    ''' route for provider clinicians '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    class ClinicianForm(forms.ModelForm):
        class Meta:
            model = Clinician
            exclude = ('work_timings', 'break_timings', 'vacations', 'experience', 'user')

    class ProviderForm(forms.ModelForm):
        class Meta:
            model = Provider
            fields = ('clinicians',)

        def __init__(self, *args, **kwargs):
            super(ProviderForm, self).__init__(*args, **kwargs)
            self.fields['clinicians'].widget = forms.CheckboxSelectMultiple()
            self.fields['clinicians'].queryset = p.clinicians.all()

    edit_form = ProviderForm(instance=p)

    if request.method == "POST":
        if request.POST['type'] == 'add':
            u = UserForm(request.POST, request.FILES).save(commit=False)
            u.password = make_password(u.password)
            u.save()
            c = ClinicianForm(request.POST, request.FILES).save(commit=False)
            c.user = u
            c.save()
            p.clinicians.add(c)

        if request.POST['type'] == 'edit':
            h = ProviderForm(request.POST, request.FILES, instance=p)
            if h.is_valid():
                h.save()
            else:
                errors += [h.errors]
            edit_form = h

    return render(request, 'healthprovider/dashboard/clinician.html.j2', context={
        "title": "Clinicians",
        "form_user": UserForm(),
        "form_clinician": ClinicianForm(),
        "form_clinician_edit": edit_form,
    })

@match_role("healthprovider")
def appointments(request):
    ''' route for dahsboard doctors list '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()
    states = [('pending', 'warning'), ('confirmed', 'success'), ('cancelled', 'danger'), ('rescheduled', 'info')]

    appointments = {}
    for state in states:
        appointments[state[0]] = {
            'queryset': p.appointment_set.filter(status=state[0]).order_by('date', 'time').all(),
            'color': state[1],
        }

    return render(request, 'healthprovider/dashboard/appointment.html.j2', context={
        "title": "Appointment List",
        "appointments": appointments.items(),
    })

# NEW ROUTES

@match_role("healthprovider")
def dashboard_home(request):
    ''' route for dashboard home  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    return render(request, 'healthprovider/dashboard/index.html.j2', context={
        'title' : "Dashboard - Home",
    })

# account routes

@match_role("healthprovider")
def account_basic(request):
    ''' route for account - basic  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    class ProviderForm(forms.ModelForm):
        class Meta:
            model = Provider
            fields = ('name',)
            labels = {
                'name': _('Hospital')
            }

    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('name', 'email', 'mobile')

    if request.method == "POST":
        poc = UserForm(request.POST, instance=p.poc)
        # provider = ProviderForm(request.POST, instance=p)

        if poc.is_valid():
            p.poc = poc.save()
            p.name = request.POST['hospital']
            p.save()

    return render(request, 'healthprovider/dashboard/account/basic.html.j2', context={
        'title' : "account - Basic",
        'hospital' : p.name,
        'user_form' : UserForm(instance=p.poc),
    })

#------------------------------------------------------------------------------------
@match_role("healthprovider")
def account_contact(request):
	''' route for account - contact  '''

@method_decorator(match_role("healthprovider"), name="dispatch")
class ContactTableView(DatatableView):
    model = User

    class datatable_class(Datatable):
        button = TextColumn('Confirm/Cancel', None, processor='get_button_raw')

        class Meta:
            columns = ['name', 'email', 'mobile', 'button']

        def get_button_raw(self, instance, **kwargs):
            if instance.status == 'pending':
                return '''
                <p>
                    <a href="/healthprovider/dashboard/contact/update/{}" class="datatable-btn btn btn-success" role="button">Update</a>
                    <a href="/healthprovider/dashboard/contact/delete/{}" class="datatable-btn btn btn-danger" role="button">Delete</a>
                </p>
                '''.format(instance.id, instance.id)

            return 'NA'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Details'
        context['healthprovider'] = get_provider(self.request.session['email'])
        return context

    def get_template_names(self):
        return 'healthprovider/dashboard/basic/contact.html.j2'

    def get_queryset(self):
        # p = get_provider(self.request.session['email'])
        # return Appointment.objects.order_by('time', 'date').filter(provider=p)
        return



@csrf_exempt
@match_role("healthprovider")
def account_contact(request):
    me = User.objects.get(pk=request.session['pk'])
    p = me.provider_set.filter(poc__id=request.session['pk']).first()

    if request.method == "POST":
        data = parser.parse(request.POST.urlencode())
        place = data['place']
        place['address_components'] = list(place['address_components'].values())
        for comp in place['address_components']:
            comp['types'] = comp['types']['']
            if isinstance(comp['types'], str):
                comp['types'] = [comp['types']]
        print(json.dumps(place, indent=4))
        try:
            l = Location(place=place)
            l.save()
            status = True
            data = place
        except Exception as e:
            print(e)
            temp_loc = Location.objects.filter(full_name__icontains=place['formatted_address']).first()
            l = temp_loc or p.location
            if l == p.location:
                status = True
                data = ["Same Location as before!"]
            elif temp_loc is None:
                status = False
                data = [str(e)]
            else:
                status = True
                data = l

        p.location = l
        p.save()

        if isinstance(data, Location):
            class LocationSerializer(ModelSerializer):
                class Meta:
                    depth = 1
                    fields = ('lat', 'long', 'full_name', 'name',)
                    model = Location
            data = LocationSerializer(data).data

        return JsonResponse({
            'status' : status,
            'data' : data,
        })

    return render(request, 'healthprovider/dashboard/account/contact.html.j2', {
        'title' : "Account - Location Settings",
        'hospital' : p,

    })



@match_role("healthprovider")
def account_speciality(request):

    ''' route for account - speciality  '''

    u = Provider.objects.filter(poc__email=request.session['email']).first()
    s = u.specialities.all()  # type: object
    class SpecialityForm(forms.ModelForm):
        class Meta:
            model = Speciality
            fields = ('name', 'description',)
    v = SpecialityForm()
    if request.method == "POST":
        b = SpecialityForm(request.POST, request.FILES)
        if b.is_valid():
            speciality = b.save()
            u.specialities.add(speciality)
            u.save()
        else:
            v = v

    return render(request, 'healthprovider/dashboard/account/speciality.html.j2', context={
        'title' : "account - speciality",
        "speciality_form" : v,
        "speciality_list" : s,
    })


#------------------------------------------------------------

@match_role("healthprovider")
def account_facilities(request):
    ''' route for account - facilities  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()
    if not p.facilities:
        p.facilities = []

    if request.method == "POST":
        print(request.POST)
        r = request.POST.dict()
        del r['csrfmiddlewaretoken']
        s = json.dumps(r)
        p.facilities.append(s)
        p.save()

    x = [json.loads(r) for r in p.facilities]


    return render(request, 'healthprovider/dashboard/account/facilities.html.j2', context={
        'title' : "account - facilities",
        'facilities' : x,
    })


@match_role("healthprovider")
def account_offerings(request):
    ''' route for account - offerings  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()
    if not p.offerings:
        p.offerings = []

    if request.method == "POST":
        print(request.POST)
        r = request.POST.dict()
        del r['csrfmiddlewaretoken']
        s = json.dumps(r)
        p.offerings.append(s)
        p.save()

    x = [json.loads(r) for r in p.offerings]


    return render(request, 'healthprovider/dashboard/account/offerings.html.j2', context={
        'title' : "account - offerings",
        'offerings': x,
    })


@match_role("healthprovider")
def account_special_checks(request):
    ''' route for account - special_checks  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()
    if not p.special_checks:
        p.special_checks = []

    if request.method == "POST":
        print(request.POST)
        r = request.POST.dict()
        del r['csrfmiddlewaretoken']
        s = json.dumps(r)
        p.special_checks.append(s)
        p.save()

    x = [json.loads(r) for r in p.special_checks]


    return render(request, 'healthprovider/dashboard/account/special_checks.html.j2', context={
        'title' : "account - special_checks",
        'special_checks': x,
    })


# Branch Routes


@match_role("healthprovider")
def branch_new(request):
    ''' route for branch - new  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    class BranchForm(forms.ModelForm):
        class Meta:
            model = Provider
            fields = ('name', 'type',)

    if request.method == "POST":
        new_branch = BranchForm(request.POST, request.FILES)
        if new_branch.is_valid():
            branch = new_branch.save(commit=False)
            branch.is_branch = True
            branch.parent_provider = p
            branch.poc = p.poc
            branch.save()
            return redirect("healthprovider:branch_view")

    return render(request, 'healthprovider/dashboard/branch/new.html.j2', context={
        'title' : "branch - new",
    })


@csrf_exempt
@match_role("healthprovider")
def branch_view(request):
    ''' route for branch - view  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    if request.method == "POST":
        b_id = request.POST['b_id']
        print('b_id', b_id)
        branch = p.provider_set.filter(pk=b_id).first()
        if branch:
            for branch_appointments in branch.appointment_set.all():
                for branch_feedbacks in branch.feedback_set.all():
                    branch_feedbacks.delete()
                branch_appointments.delete()
            branch.delete()
            return HttpResponse("Branch successfully deleted!")
        else:
            return HttpResponse("Invalid Branch!")

    branches = p.provider_set.all()

    return render(request, 'healthprovider/dashboard/branch/view.html.j2', context={
        'title' : "branch - view",
        'branches' : branches,
    })


# branch update routes


@match_role("healthprovider")
def branch_basic(request):
    ''' route for branch update - branch_basic'''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/branch/branch_basic.html.j2', context={
        'title' : "Update - branch_basic"
    })


@match_role("healthprovider")
def branch_contact(request):
    ''' route for branch update - branch_contact'''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/branch/branch_contact.html.j2', context={
        'title' : "Update - branch_contact"
    })


@match_role("healthprovider")
def branch_facilities(request):
    ''' route for branch update - branch_facilities'''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/branch/branch_facilities.html.j2', context={
        'title' : "Update - branch_facilities"
    })


@match_role("healthprovider")
def branch_healthcheck(request):
    ''' route for branch update - branch_healthcheck'''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/branch/branch_healthcheck.html.j2', context={
        'title' : "Update - branch_healthcheck"
    })


@match_role("healthprovider")
def branch_offerings(request):
    ''' route for branch update - branch_offerings'''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/branch/branch_offerings.html.j2', context={
        'title' : "Update - branch_offerings"
    })


@match_role("healthprovider")
def branch_organization(request):
    ''' route for branch update - branch_organization'''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/branch/branch_organization.html.j2', context={
        'title' : "Update - branch_organization"
    })


@match_role("healthprovider")
def branch_speciality(request):
    ''' route for branch update - branch_speciality'''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/branch/branch_speciality.html.j2', context={
        'title' : "Update - branch_speciality"
    })



# Appointment Routes

@method_decorator(match_role("healthprovider"), name="dispatch")
class AppointmentTableView(DatatableView):
    model = Appointment

    class datatable_class(Datatable):
        time_parsed = DateTimeColumn('Time', None, processor='get_time')
        status_new = TextColumn('Status', None, processor='get_status_raw')
        button = TextColumn('Confirm/Cancel', None, processor='get_button_raw')

        class Meta:
            columns = ['date', 'time_parsed', 'provider', 'status_new', 'button']
            labels = {
                'date': 'Date',
                'provider': 'Provider',
            }
            processors = {
                'provider': 'get_provider_name',
            }

        def get_button_raw(self, instance, **kwargs):
            if instance.status == 'pending':
                return '''
                <p>
                    <a href="/healthprovider/dashboard/appointments/confirm/{}" class="datatable-btn btn btn-success" role="button">Confirm</a>
                    <a href="/healthprovider/dashboard/appointments/cancel/{}" class="datatable-btn btn btn-danger" role="button">Cancel</a>
                </p>
                '''.format(instance.id, instance.id)

            return 'NA'

        def get_status_raw(self, instance, **kwargs):
            if instance.status == 'confirmed':
                return '''
                <p>
                    <a href="#" class="datatable-btn btn btn-success disabled" role="button">Confirmed</a>
                </p>
                '''

            elif instance.status == 'cancelled':
                return '''
                <p>
                    <a href="#" class="datatable-btn btn btn-danger disabled" role="button">Cancelled</a>
                </p>
                '''

            return '''
            <p>
                <a href="#" class="datatable-btn btn btn-warning disabled" role="button">Pending</a>
            </p>
            '''

        def get_provider_name(self, instance, **kwargs):
            return instance.provider.name

        def get_time(self, instance, **kwargs):
            time = instance.time
            m = 'PM' if int(time.hour / 12) else 'AM'
            return '{}:{} {}'.format(time.hour % 12, time.minute, m)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Appointments'
        context['healthprovider'] = get_provider(self.request.session['email'])
        return context

    def get_template_names(self):
        return 'healthprovider/dashboard/appointments/daily.html.j2'

    def get_queryset(self):
        today = datetime.date.today()
        p = get_provider(self.request.session['email'])
        # return Appointment.objects.order_by('time', 'date').filter(under=c).filter(date__gte=today)
        return Appointment.objects.order_by('time', 'date').filter(provider=p)


@match_role("healthprovider")
def confirm_appointment(request, id):
    p = get_provider(request.session['email'])
    a = Appointment.objects.filter(id=id).first()

    # return JsonResponse({'provider': a.provider.id, 'user': p.id})

    if a.provider == p:
        a.status = 'confirmed'
        a.save()
    else:
        # add appropriate error handling
        print("*** Authorization failed ***")
        return JsonResponse({'status': 'Auth Error'})

    return redirect('healthprovider:appointment_daily')


@match_role("healthprovider")
def cancel_appointment(request, id):
    p = get_provider(request.session['email'])
    a = Appointment.objects.filter(id=id).first()

    if a.provider == p:
        a.status = 'cancelled'
        a.save()
    else:
        # add appropriate error handling
        print("*** Authorization failed ***")
        return JsonResponse({'status': 'Auth Error'})

    return redirect('healthprovider:appointment_daily')


@match_role("healthprovider")
def appointment_weekly(request):
    ''' route for appointment - weekly  '''

    today = datetime.date.today()
    p = Provider.objects.filter(poc__email=request.session['email']).first()

    days = []
    for d in range(7):
        day = today + datetime.timedelta(days=d)
        days.append({
            'name': day.strftime('%A'),
            'date': day.strftime('%d-%m-%Y'),
            'n_pending': p.appointment_set.filter(date=day).filter(status='pending').count(),
            'n_confirmed': p.appointment_set.filter(date=day).filter(status='confirmed').count(),
            'n_cancelled': p.appointment_set.filter(date=day).filter(status='cancelled').count(),
        })

    return render(request, 'healthprovider/dashboard/appointments/weekly.html.j2', context={
        'title': "appointment - weekly",
        'days': days
    })


@match_role("healthprovider")
def appointment_monthly(request):
    ''' route for appointment - monthly  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/appointments/monthly.html.j2', context={
        'title' : "appointment - monthly",
        'doctors' : p.clinicians.all(),
    })


# Payment Routes


@match_role("healthprovider")
def payment_new(request):
    """ route for payment - new  """

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/payment/new.html.j2', context={
        'title' : "payment - new",
    })


@match_role("healthprovider")
def payment_add(request):
    ''' route for payment - add  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()


    return render(request, 'healthprovider/dashboard/payment/add.html.j2', context={
        'title' : "payment - add",
    })


@match_role("healthprovider")
def payment_view(request):
    ''' route for payment - view  '''

    p = Provider.objects.filter(poc__email=request.session['email']).first()

    trans = Transaction.objects.filter(sender=p.poc).all()

    return render(request, 'healthprovider/dashboard/payment/view.html.j2', context={
        'title' : "payment - view",
        'transactions' : trans,
    })


# Clinician Routes

@match_role("healthprovider")
def clinician_new(request):
    """ route for clinician - new  """

    p = Provider.objects.filter(poc__email=request.session['email']).first()
    user_form = UserForm()

    if request.method == 'POST':
        u = UserForm(request.POST, request.FILES)
        if u.is_valid():
            user = u.save(commit=False)
            user.password = make_password(request.POST['password'])
            user.role = 'clinician'
            user.save()
            c = Clinician()
            c.user = user
            c.save()
            print(c)
            p.clinicians.add(c)
            p.save()

    return render(request, 'healthprovider/dashboard/clinicians/new.html.j2', context={
        'title': "clinician - new",
        'form': user_form,
    })



@method_decorator(match_role("healthprovider"), name="dispatch")
class ClinicianTableView(DatatableView):
    model = Clinician

    class datatable_class(Datatable):
        user_name = TextColumn('Doctor\'s Name', None, processor='get_clinician_name')
        user_email = TextColumn('Email', None, processor='get_clinician_email')
        user_mobile = TextColumn('Mobile', None, processor='get_clinician_mobile')
        specialities_parsed = TextColumn('Specialities', None, processor='get_specialities')

        class Meta:
            columns = ['user_name', 'user_email', 'user_mobile', 'specialities_parsed']

        def get_clinician_name(self, instance, **kwargs):
            return instance.user.name

        def get_clinician_email(self, instance, **kwargs):
            return instance.user.email

        def get_clinician_mobile(self, instance, **kwargs):
            return instance.user.mobile

        def get_specialities(self, instance, **kwargs):
            # need to work on this
            # return instance.specialities
            return 'Speciality'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clinicians'
        context['healthprovider'] = get_provider(self.request.session['email'])
        return context

    def get_template_names(self):
        return 'healthprovider/dashboard/clinicians/view.html.j2'

    def get_queryset(self):
        p = get_provider(self.request.session['email'])
        return p.clinicians.all()

@match_role("healthprovider")
def account_work_time(request):
    ''' work timing routes for clinician '''
    me = User.objects.filter(email=request.session['email']).first()
    print(me)
    c = Provider.objects.filter(poc__email=me).first()
    print(c.name)
    days = ["Sunday", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday"]
    if request.method == "POST":
        p_dict = parser.parse(request.POST.urlencode())
        timings = []
        work_timings = c.work_timings
        base_compare = c.work_timings
        assert (len(days) == len(work_timings))
        for day, actual in zip(days, base_compare):
            try:
                timings.append(list(map(lambda x: datetime.datetime.strptime(x,
                                                                             '%H:%M:%S').time(),
                                        p_dict['timings'][day])))
            except ValueError:
                try:
                    timings.append(list(map(lambda x: datetime.datetime.strptime(x,
                                                                                 '%H:%M').time(),
                                            p_dict['timings'][day])))
                except KeyError:
                    timings.append(actual)
            except KeyError:
                timings.append(actual)

        c.work_timings = timings
        c.save()

    work_timings = []
    if c.work_timings:
        for day, w_t in zip(days, c.work_timings):
            cur_obj = {'day': day}
            cur_obj['start'] = w_t[0].isoformat().split('.')[0][:5]
            cur_obj['end'] = w_t[-1].isoformat().split('.')[0][:5]
            work_timings.append(cur_obj)

    return render(request, 'healthprovider/dashboard/account/worktime.html.j2', context={
        'title': "Timings - Work timings",
        'provider': c,
        'timings': work_timings,
        'days' :days,
    })


@match_role("healthprovider")
def account_amenity(request):
    provider_object = Provider.objects.filter(poc__email=request.session['email']).first()
    amenity_objects = Amenity.objects.all()  # type: object
    if request.method == "POST":
        list_amenity_ids = request.POST.getlist('amenity')
        for amenity in list_amenity_ids:
            provider_object.amenities.add(amenity)
        provider_object.save()
        print(provider_object)
    return render(request, 'healthprovider/dashboard/account/amenity.html.j2', {'s': amenity_objects})