import datetime
import json

from datatableview import (Datatable, DateTimeColumn, TextColumn,
                           ValuesDatatable)
from datatableview.helpers import make_xeditable
from datatableview.views import DatatableView, XEditableDatatableView
from django import forms
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from querystring_parser import parser

from api.models import Appointment, Clinician, Speciality, User
from phealth.utils import get_clinician, match_role, signin
from .forms import *


# Create your views here.

def SignIn(request):
    if request.method == "GET":
        return render(request, 'common/signin.html.j2', context={
            "title": "Admin Login",
            "route": "/admin",
            "color": "info"
        })
    elif request.method == "POST":
        # print(request.POST)
        if signin("admin", request):
            return redirect('site_admin:dashboard_home_new')
        return redirect('site_admin:signin')


def SignUp(request):
    ''' no signin functionality for the admin
	'''
    return redirect('site_admin:signin')


# Dashboard view functions

@match_role("admin")
def dashboard(request):
    ''' route for dashboard home '''

    u = User.objects.filter(user__email=request.session['email']).first()
    v = u.user

    class ClinicianForm(forms.ModelForm):

        class Meta:
            model = Clinician
            fields = ('education', 'experience')

    class UserForm(forms.ModelForm):

        class Meta:
            model = User
            fields = ('name', 'email', 'mobile', 'gender',
                      'question', 'answer', 'profile_pic')

    if request.method == "POST":
        c = ClinicianForm(request.POST, request.FILES, instance=u)
        b = UserForm(request.POST, request.FILES, instance=v)
        if c.is_valid() and b.is_valid():
            c.save() and b.save()

    return render(request, 'clinician/dashboard/home.html.j2', context={
        "title": "Dashboard Home",
        "form_title": "Edit basic information",
        "clinician_form": ClinicianForm(instance=u),
        "user_form": UserForm(instance=v),
    })


@match_role("admin")
def speciality(request):
    u = User.objects.filter(user__email=request.session['email']).first()
    n = u.specialities.all()

    # print("I was here")
    class SpecialityForm(forms.ModelForm):
        class Meta:
            model = Speciality
            fields = ('name', 'description',)

    v = SpecialityForm()
    if request.method == "POST":
        b = SpecialityForm(request.POST, request.FILES)
        if b.is_valid():
            u.save()
            speciality = b.save()
            # speciality.save()
            u.specialities.add(speciality)
        else:
            v = b

    return render(request, 'site_admin/dashboard/speciality.html.j2', context={
        "title": "Speciality Addition",
        "speciality_form": v,
        "speciality_list": n,
    })


@match_role("admin")
def appointments(request):
    c = User.objects.filter(user__email=request.session['email']).first()
    apps = Appointment.objects.filter(under=c).all().order_by('id')
    appointments_arr = []

    class AppointmentForm(forms.ModelForm):

        class Meta:
            model = Appointment
            fields = ('status',)

    for appointment in apps:
        appointments_arr.append((appointment, AppointmentForm(instance=appointment)))

    if request.method == 'POST':
        print(request.POST)
        b = AppointmentForm(request.POST, request.FILES,
                            instance=Appointment.objects.filter(id=int(request.POST['appointment'])).first())
        if b.is_valid():
            b.save()
            print(b)

    return render(request, 'site_admin/dashboard/appointments.html.j2', context={
        "title": "Doctors Appointment List",
        "appointments": appointments_arr,
    })


@match_role("admin")
def calender(request):
    ''' dashboard function '''
    ''' handles the calender page for clincian timings
	and bookings
	'''
    c = User.objects.filter(user__email=request.session['email']).first()
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    if request.method == "POST":
        p_dict = parser.parse(request.POST.urlencode())
        if p_dict['section'] in ['work', 'break']:
            timings = []
            if p_dict['section'] == 'work':
                base_compare = c.work_timings
            else:
                base_compare = c.break_timings
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
            if p_dict['section'] == 'work':
                c.work_timings = timings
            else:
                c.break_timings = timings
        else:
            try:
                vacs = p_dict['timings'][""]
                vacs = [list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
                                 [i, j])) for i, j in zip(vacs[::2], vacs[1::2])]
                c.vacations = vacs
            except:
                pass
        c.save()

    work_timings, break_timings, vacation_timings = [], [], []

    for day, w_t, b_t in zip(days, c.work_timings, c.break_timings):
        cur_obj = {'day': day}
        cur_obj['start'] = w_t[0].isoformat().split('.')[0][:5]
        cur_obj['end'] = w_t[-1].isoformat().split('.')[0][:5]
        work_timings.append(cur_obj)
        cur_obj['start'] = b_t[0].isoformat().split('.')[0][:5]
        cur_obj['end'] = b_t[-1].isoformat().split('.')[0][:5]
        break_timings.append(cur_obj)

    for vacation in c.vacations:
        vacation_timings.append({
            'start': vacation[0].isoformat(),
            'end': vacation[-1].isoformat(),
        })

    return render(request, 'site_admin/dashboard/calender.html.j2', context={
        'title': "Set your timings",
        'work': work_timings,
        'break': break_timings,
        'vacations': vacation_timings,
    })


# NEW ROUTES Defined

@match_role("admin")
def new_home(request):
    return render(request, 'site_admin/dashboard/new_home.html', {})

    ''' new dashboard home 

    c = User.objects.filter(user__email=request.session['email'])
    return render(request, 'site_admin/dashboard/index.html', context={
        'title': "Admin Home",
        'admin': c,
    }) '''


@match_role("admin")
def new_home(request):
    return render(request, 'site_admin/dashboard/new_home.html', {})


@match_role("admin")
def cms_add(request):
    return render(request, 'site_admin/dashboard/cms_add.html', {})


@match_role("admin")
def cms_view(request):
    return render(request, 'site_admin/dashboard/cms_view.html', {})

#conditions
@match_role("admin")
def condition_add(request):
    if request.method == 'POST':
        form = SymptomsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:condition_view')
    else:
        form = SymptomsForm()
    return render(request, 'site_admin/dashboard/condition_add.html', {'form': form})

@match_role("admin")
def condition_view(request):
    result = Symptoms.objects.all()
    return render(request, 'site_admin/dashboard/condition_view.html', {'values': result})

@match_role("admin")
def condition_edit(request, pk):
    post = get_object_or_404(Symptoms, pk=pk)
    if request.method == "POST":
        form = SymptomsForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:condition_view')
    else:
        form = SymptomsForm(instance=post)
    return render(request, 'site_admin/dashboard/condition_add.html', {'form': form})

@match_role("admin")
def condition_delete(request, pk):
    result = Symptoms.objects.get(pk=pk)
    result.delete()
    return redirect('site_admin:condition_view')

@match_role("admin")
def timesession_add(request):
    return render(request, 'site_admin/dashboard/timesession_add.html', {})


@match_role("admin")
def timesession_view(request):
    return render(request, 'site_admin/dashboard/timesession_view.html', {})


@match_role("admin")
def speciality_add(request):
    return render(request, 'site_admin/dashboard/speciality_add.html', {})


@match_role("admin")
def speciality_view(request):
    return render(request, 'site_admin/dashboard/speciality_view.html', {})


@match_role("admin")
def coupons_add(request):
    return render(request, 'site_admin/dashboard/coupons_add.html', {})


@match_role("admin")
def coupons_view(request):
    return render(request, 'site_admin/dashboard/coupons_view.html', {})


@match_role("admin")
def coupons_reports(request):
    return render(request, 'site_admin/dashboard/coupons_reports.html', {})

#-------------------------------------------------------------------------------
@match_role("admin")
def test_add(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:test_view')
    else:
        form = TestForm()
    return render(request, 'site_admin/dashboard/test_add.html', {'form': form})


@match_role("admin")
def test_view(request):
    result = Test.objects.all()
    return render(request, 'site_admin/dashboard/test_view.html', {'values': result})

@match_role("admin")
def test_edit(request, pk):
    post = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        form = TestForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:test_view')
    else:
        form = TestForm(instance=post)
    return render(request, 'site_admin/dashboard/test_add.html', {'form': form})

@match_role("admin")
def test_delete(request, pk):
    result = Test.objects.get(pk=pk)
    result.delete()
    return redirect('site_admin:test_view')


#------------------------------------------------------------------------------>
@match_role("admin")
def test_category_add(request):
    return render(request, 'site_admin/dashboard/test_category_add.html', {})


@match_role("admin")
def test_category_view(request):
    return render(request, 'site_admin/dashboard/test_category_view.html', {})


@match_role("admin")
def test_subcategory_add(request):
    return render(request, 'site_admin/dashboard/test_subcategory_add.html', {})


@match_role("admin")
def test_subcategory_view(request):
    return render(request, 'site_admin/dashboard/test_subcategory_view.html', {})


@match_role("admin")
def facility_type_add(request):
    return render(request, 'site_admin/dashboard/facility_type_add.html', {})


@match_role("admin")
def facility_type_view(request):
    return render(request, 'site_admin/dashboard/facility_type_view.html', {})


@match_role("admin")
def facility_add(request):
    return render(request, 'site_admin/dashboard/facility_add.html', {})


@match_role("admin")
def facility_view(request):
    return render(request, 'site_admin/dashboard/facility_view.html', {})


@match_role("admin")
def roles_add(request):
    return render(request, 'site_admin/dashboard/roles_add.html', {})


@match_role("admin")
def roles_view(request):
    return render(request, 'site_admin/dashboard/roles_view.html', {})


@match_role("admin")
def idconfiguration_add(request):
    return render(request, 'site_admin/dashboard/idconfiguration_add.html', {})


@match_role("admin")
def idconfiguration_view(request):
    return render(request, 'site_admin/dashboard/idconfiguration_view.html', {})


@match_role("admin")
def users(request):
    return render(request, 'site_admin/dashboard/users.html', {})


@match_role("admin")
def salesagents_add(request):
    return render(request, 'site_admin/dashboard/salesagents_add.html', {})


@match_role("admin")
def salesagents_view(request):
    return render(request, 'site_admin/dashboard/salesagents_view.html', {})


@match_role("admin")
def health_daily(request):
    return render(request, 'site_admin/dashboard/health_daily.html', {})


@match_role("admin")
def health_weekly(request):
    return render(request, 'site_admin/dashboard/health_weekly.html', {})


@match_role("admin")
def health_monthly(request):
    return render(request, 'site_admin/dashboard/health_monthly.html', {})

#---------------------Dicount Cards------------------------------------------------------------
@match_role("admin")
def discountcard_add(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:discountcard_view')
    else:
        form = DiscountForm()
    return render(request, 'site_admin/dashboard/discountcard_add.html', {'form': form})


@match_role("admin")
def discountcard_view(request):
    result = DiscountCard.objects.all()
    return render(request, 'site_admin/dashboard/discountcard_view.html', {'values': result})

@match_role("admin")
def discountcard_edit(request, pk):
    post = get_object_or_404(DiscountCard, pk=pk)
    if request.method == "POST":
        form = DiscountForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:discountcard_view')
    else:
        form = DiscountForm(instance=post)
    return render(request, 'site_admin/dashboard/discountcard_add.html', {'form': form})

@match_role("admin")
def dicountcard_delete(request, pk):
    result = DiscountCard.objects.get(pk=pk)
    result.delete()
    return redirect('site_admin:discountcard_view')


@match_role("admin")
def discountcard_reports(request):
    result = DiscountCard.objects.all()
    return render(request, 'site_admin/dashboard/discountcard_reports.html', {})

#-------------------------------Healthcheckups---------------------------------------------------------------------
@match_role("admin")
def healthcheck_add(request):
    if request.method == 'POST':
        form = HealthCheckupForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:healthcheck_view')
    else:
        form = HealthCheckupForm()
    return render(request, 'site_admin/dashboard/healthcheck_add.html', {'form': form})


@match_role("admin")
def healthcheck_view(request):
    result = HealthCheckup.objects.all()
    return render(request, 'site_admin/dashboard/healthcheck_view.html', {'values': result})

@match_role("admin")
def healthcheck_edit(request, pk):
    post = get_object_or_404(HealthCheckup, pk=pk)
    if request.method == "POST":
        form = HealthCheckupForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:healthcheck_view')
    else:
        form = DiscountForm(instance=post)
    return render(request, 'site_admin/dashboard/healthcheck_add.html', {'form': form})

@match_role("admin")
def healthcheck_delete(request, pk):
    result = HealthCheckup.objects.get(pk=pk)
    result.delete()
    return redirect('site_admin:healthcheck_view')



@match_role("admin")
def healthcheck_reports(request):
    return render(request, 'site_admin/dashboard/healthcheck_reports.html', {})


@match_role("admin")
def healthprovider_plans_add(request):
    return render(request, 'site_admin/dashboard/healthprovider_plans_add.html', {})


@match_role("admin")
def healthprovider_plans_view(request):
    return render(request, 'site_admin/dashboard/healthprovider_plans_view.html', {})


@match_role("admin")
def healthprovider_plans_reports(request):
    return render(request, 'site_admin/dashboard/healthprovider_plans_reports.html', {})

#------------------------------------------------------------------------------------------------------------------------
@match_role("admin")
def salesagents_packages_add(request):
    return render(request, 'site_admin/dashboard/salesagents_packages_add.html', {})


@match_role("admin")
def salesagents_packages_view(request):
    return render(request, 'site_admin/dashboard/salesagents_packages_view.html', {})


@match_role("admin")
def salesagents_packages_reports(request):
    return render(request, 'site_admin/dashboard/salesagents_packages_reports.html', {})


@match_role("admin")
def resellers_packages_add(request):
    return render(request, 'site_admin/dashboard/resellers_packages_add.html', {})


@match_role("admin")
def resellers_packages_view(request):
    return render(request, 'site_admin/dashboard/resellers_packages_view.html', {})


@match_role("admin")
def resellers_packages_reports(request):
    return render(request, 'site_admin/dashboard/resellers_packages_reports.html', {})


# appointment routes

@method_decorator(match_role("admin"), name="dispatch")
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
					<a href="/admin/dashboard/appointments/confirm/{}" class="datatable-btn btn btn-success" role="button">Confirm</a>
					<a href="/admin/dashboard/appointments/cancel/{}" class="datatable-btn btn btn-danger" role="button">Cancel</a>
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
        context['admin'] = get_clinician(self.request.session['email'])
        return context

    def get_template_names(self):
        return 'site_admin/dashboard/appointments/daily.html.j2'

    def get_queryset(self):
        today = datetime.date.today()
        c = get_clinician(self.request.session['email'])
        # return Appointment.objects.order_by('time', 'date').filter(under=c).filter(date__gte=today)
        return Appointment.objects.order_by('time', 'date').filter(under=c)


@match_role("admin")
def confirm_appointment(request, id):
    c = get_clinician(request.session['email'])
    a = Appointment.objects.filter(id=id).first()

    if a.under == c:
        a.status = 'confirmed'
        a.save()
    else:
        # add appropriate error handling
        print("*** Authorization failed ***")
        return JsonResponse({'status': 'Auth Error'})

    return redirect('site_admin:appointment_daily')


@match_role("admin")
def cancel_appointment(request, id):
    c = get_clinician(request.session['email'])
    a = Appointment.objects.filter(id=id).first()

    if a.under == c:
        a.status = 'cancelled'
        a.save()
    else:
        # add appropriate error handling
        print("*** Authorization failed ***")
        return JsonResponse({'status': 'Auth Error'})

    return redirect('site_admin:appointment_daily')


@match_role("admin")
def appointment_weekly(request):
    ''' appointment stats '''

    today = datetime.date.today()
    c = User.objects.filter(user__email=request.session['email']).first()

    days = []
    for d in range(7):
        day = today + datetime.timedelta(days=d)
        days.append({
            'name': day.strftime('%A'),
            'date': day.strftime('%d-%m-%Y'),
            'n_pending': c.appointment_set.filter(date=day).filter(status='pending').count(),
            'n_confirmed': c.appointment_set.filter(date=day).filter(status='confirmed').count(),
            'n_cancelled': c.appointment_set.filter(date=day).filter(status='cancelled').count(),
        })

    return render(request, 'site_admin/dashboard/appointments/weekly.html.j2', context={
        'title': "appointment - weekly",
        'admin': c,
        'days': days
    })


@match_role("admin")
def appointment_monthly(request):
    ''' appointment stats '''

    c = User.objects.filter(user__email=request.session['email']).first()

    return render(request, 'site_admin/dashboard/appointments/monthly.html.j2', context={
        'title': "appointment - monthly",
        'admin': c,
    })


# timings routes


@match_role("admin")
def timing_work(request):
    ''' work timing routes for admin '''

    c = User.objects.filter(user__email=request.session['email']).first()

    work_timings = c.work_timings
    days = ["Sunday", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday"]
    assert (len(days) == len(work_timings))
    if request.method == "POST":
        p_dict = parser.parse(request.POST.urlencode())
        timings = []
        base_compare = c.work_timings
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

    for day, w_t in zip(days, c.work_timings):
        cur_obj = {'day': day}
        cur_obj['start'] = w_t[0].isoformat().split('.')[0][:5]
        cur_obj['end'] = w_t[-1].isoformat().split('.')[0][:5]
        work_timings.append(cur_obj)

    return render(request, 'site_admin/dashboard/timings/worktime.html.j2', context={
        'title': "Timings - Work timings",
        'admin': c,
        'timings': work_timings,
    })


@match_role("admin")
def timing_break(request):
    ''' break timings routes for admin '''

    c = User.objects.filter(user__email=request.session['email']).first()

    days = ["Sunday", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday"]

    if request.method == "POST":
        p_dict = parser.parse(request.POST.urlencode())
        timings = []
        base_compare = c.break_timings
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
        c.break_timings = timings
        try:
            c.save()
        except:
            pass

    break_timings = []

    for day, b_t in zip(days, c.break_timings):
        cur_obj = {'day': day}
        cur_obj['start'] = b_t[0].isoformat().split('.')[0][:5]
        cur_obj['end'] = b_t[-1].isoformat().split('.')[0][:5]
        break_timings.append(cur_obj)

    return render(request, 'site_admin/dashboard/timings/breaktime.html.j2', context={
        'title': "Timings -  break",
        'admin': c,
        'timings': break_timings
    })


@match_role("admin")
def timing_vacation(request):
    ''' vacations dates routes for admin '''

    c = User.objects.filter(user__email=request.session['email']).first()

    if request.method == "POST":
        p_dict = parser.parse(request.POST.urlencode())
        try:
            vacs = p_dict['timings'][""]
            vacs = [list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
                             [i, j])) for i, j in zip(vacs[::2], vacs[1::2])]
            c.vacations = vacs
        except:
            pass

    vacation_timings = []
    for vacation in c.vacations:
        vacation_timings.append({
            'start': vacation[0].isoformat(),
            'end': vacation[-1].isoformat(),
        })

    return render(request, 'site_admin/dashboard/timings/vacationtime.html.j2', context={
        'title': "Timings -  vacation",
        'admin': c,
        'timings': vacation_timings,
    })


# account routes

@match_role("admin")
def basic_details(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    u = c.user

    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('name', 'gender')

    if request.method == "POST":
        b = UserForm(request.POST, instance=u)
        if b.is_valid():
            b.save()

    return render(request, 'site_admin/dashboard/account/basic.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'form': UserForm(instance=u),
    })


@match_role("admin")
def professional_info(request):
    u = User.objects.filter(user__email=request.session['email']).first()
    n = u.specialities.all()

    class SpecialityForm(forms.ModelForm):
        class Meta:
            model = Speciality
            fields = ('name', 'description',)

    v = SpecialityForm()
    if request.method == "POST":
        b = SpecialityForm(request.POST, request.FILES)
        if b.is_valid():
            u.save()
            speciality = b.save()
            u.specialities.add(speciality)
        else:
            v = b

    return render(request, 'site_admin/dashboard/account/professionaldetails.html.j2', context={
        "title": "Account - ",
        "speciality_form": v,
        "speciality_list": n,
    })


@match_role("admin")
def education_training(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    u = c.user

    class EducationForm(forms.ModelForm):
        class Meta:
            model = User
            fields = (
                'basic_education', 'post_graduate', 'diploma', 'super_speciality', 'other_trainings', 'other_degrees',
                'profile_pic')

    if request.method == "POST":
        e = EducationForm(request.POST, request.FILES, instance=u)
        if e.is_valid():
            e.save()

    return render(request, 'site_admin/dashboard/account/education.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'form': EducationForm(instance=u),
    })


@match_role("admin")
def consultation_fee(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    u = c.user

    class FeeForm(forms.ModelForm):
        class Meta:
            model = Clinician
            fields = ('fee', 'amount', 'discount', 'discount_sub')

    if request.method == "POST":
        f = FeeForm(request.POST, request.FILES, instance=c)
        if f.is_valid():
            f.save()

    return render(request, 'site_admin/dashboard/account/consultation.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'form': FeeForm(instance=c),
    })


@match_role("admin")
def offerings(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    if not c.offerings:
        c.offerings = []
    o = c.offerings
    if request.method == "POST":
        print(request.POST)
        print(c.offerings)
        c.offerings.append(request.POST['offering'])
        c.save()
    return render(request, 'site_admin/dashboard/account/offerings.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'offerings': o,
    })


@match_role("admin")
def conditions_treated(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    ct = c.conditions_treated
    if request.method == "POST":
        print(request.POST)
        print(c.conditions_treated)
        if c.conditions_treated == None:
            c.conditions_treated = [request.POST['condition']]
        else:
            c.conditions_treated.append(request.POST['condition'])
        c.save()

    return render(request, 'site_admin/dashboard/account/conditions.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'conditions_treated': ct,
    })


@match_role("admin")
def procedures(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    p = c.procedures

    if request.method == "POST":
        print(request.POST)
        print(c.procedures)
        if c.procedures == None:
            c.procedures = [request.POST['procedure']]
        else:
            c.procedures.append(request.POST['procedure'])
        c.save()

    return render(request, 'site_admin/dashboard/account/procedures.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'procedures': p,
    })


@match_role("admin")
def experience(request):
    ''' account route for '''
    c = User.objects.filter(user__email=request.session['email']).first()
    if not c.experience:
        c.experience = []
    e = c.experience

    if request.method == "POST":
        r = request.POST.dict()
        del r['csrfmiddlewaretoken']
        s = json.dumps(r)
        e.append(s)
        c.save()

    # del e[0]
    x = [json.loads(r) for r in e]
    return render(request, 'site_admin/dashboard/account/experience.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'experiences': x,
    })


@match_role("admin")
def awards_recognition(request):
    ''' account route for '''
    c = User.objects.filter(user__email=request.session['email']).first()
    if not c.awards:
        c.awards = []

    if request.method == "POST":
        print(request.POST)
        r = request.POST.dict()
        del r['csrfmiddlewaretoken']
        s = json.dumps(r)
        c.awards.append(s)
        c.save()

    x = [json.loads(r) for r in c.awards]
    return render(request, 'site_admin/dashboard/account/awards.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'awards': x
    })


@match_role("admin")
def registrations(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    if not c.registrations:
        c.registrations = []

    if request.method == "POST":
        print(request.POST)
        r = request.POST.dict()
        del r['csrfmiddlewaretoken']
        s = json.dumps(r)
        c.registrations.append(s)
        c.save()

    x = [json.loads(r) for r in c.registrations]

    return render(request, 'site_admin/dashboard/account/registration.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'registrations': x,
    })


@match_role("admin")
def memberships(request):
    ''' account route for '''

    c = User.objects.filter(user__email=request.session['email']).first()
    if not c.memberships:
        c.memberships = []

    if request.method == "POST":
        print(request.POST)
        r = request.POST.dict()
        del r['csrfmiddlewaretoken']
        s = json.dumps(r)
        c.memberships.append(s)
        c.save()

    x = [json.loads(r) for r in c.memberships]

    return render(request, 'site_admin/dashboard/account/memberships.html.j2', context={
        'title': "Account - ",
        'admin': c,
        'memberships': x,
    })
