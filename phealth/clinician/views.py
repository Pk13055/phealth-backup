import datetime
import json

from datatableview import (Datatable, DateTimeColumn, TextColumn,
                           ValuesDatatable)
from datatableview.helpers import make_xeditable
from datatableview.views import DatatableView, XEditableDatatableView
from django import forms
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from querystring_parser import parser

from api.models import Appointment, Clinician, Speciality, User, Provider
from phealth.utils import get_clinician, match_role, signin

# Create your views here.

def SignIn(request):
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Clinician Login",
			"route": "/clinician",
			"color": "info"
		})
	elif request.method == "POST":
		if signin("clinician", request):
			return redirect('clinician:dashboard_home')
		return redirect('clinician:signin')

def SignUp(request):
	''' no signin functionality for the clinician
	'''
	return redirect('clinician:signin')


@match_role("clinician")
def new_home(request):
	''' new dashboard home '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	return render(request, 'clinician/dashboard/new_home.html.j2', context={
		'title' : "Clinician Home",
		'clinician' : c,
		})

# appointment routes

@method_decorator(match_role("clinician"), name="dispatch")
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
					<a href="/clinician/dashboard/appointments/confirm/{}" class="datatable-btn btn btn-success" role="button">Confirm</a>
					<a href="/clinician/dashboard/appointments/cancel/{}" class="datatable-btn btn btn-danger" role="button">Cancel</a>
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
		context['clinician'] = get_clinician(self.request.session['email'])
		return context

	def get_template_names(self):
		return 'clinician/dashboard/appointments/daily.html.j2'

	def get_queryset(self):
		today = datetime.date.today()
		c = get_clinician(self.request.session['email'])
		# return Appointment.objects.order_by('time', 'date').filter(under=c).filter(date__gte=today)
		return Appointment.objects.order_by('time', 'date').filter(under=c)


@match_role("clinician")
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

	return redirect('clinician:appointment_daily')


@match_role("clinician")
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

	return redirect('clinician:appointment_daily')


@match_role("clinician")
def appointment_weekly(request):
	''' appointment stats '''

	today = datetime.date.today()
	c = Clinician.objects.filter(user__email=request.session['email']).first()

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


	return render(request, 'clinician/dashboard/appointments/weekly.html.j2', context={
		'title' : "appointment - weekly",
		'clinician' : c,
		'days': days
	})



@match_role("clinician")
def appointment_monthly(request):
	''' appointment stats '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	return render(request, 'clinician/dashboard/appointments/monthly.html.j2', context={
		'title' : "appointment - monthly",
		'clinician' : c,
		})

# timings routes


@match_role("clinician")
def timing_work(request):
	''' work timing routes for clinician '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	work_timings = c.work_timings
	days = ["Sunday", "Monday", "Tuesday", "Wednesday",
	"Thursday", "Friday", "Saturday"]
	assert(len(days) == len(work_timings))
	if request.method == "POST":
		p_dict = parser.parse(request.POST.urlencode())
		timings = []
		base_compare = c.work_timings
		for day, actual in zip(days, base_compare):
			try:
				timings.append(list(map(lambda x: datetime.datetime.strptime(x,
				 '%H:%M:%S').time(), p_dict['timings'][day])))
			except ValueError:
				try:
					timings.append(list(map(lambda x: datetime.datetime.strptime(x,
				 	'%H:%M').time(), p_dict['timings'][day])))
				except KeyError:
					timings.append(actual)
			except KeyError:
				timings.append(actual)

		c.work_timings = timings
		c.save()


	work_timings = []

	for day, w_t in zip(days, c.work_timings):
		cur_obj = { 'day' : day }
		cur_obj['start'] = w_t[0].isoformat().split('.')[0][:5]
		cur_obj['end'] = w_t[-1].isoformat().split('.')[0][:5]
		work_timings.append(cur_obj)

	return render(request, 'clinician/dashboard/timings/worktime.html.j2', context={
		'title' : "Timings - Work timings",
		'clinician' : c,
		'timings' : work_timings,
		})


@match_role("clinician")
def timing_break(request):
	''' break timings routes for clinician '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	days = ["Sunday", "Monday", "Tuesday", "Wednesday",
		"Thursday", "Friday", "Saturday"]

	if request.method == "POST":
		p_dict = parser.parse(request.POST.urlencode())
		timings = []
		base_compare = c.break_timings
		for day, actual in zip(days, base_compare):
			try:
				timings.append(list(map(lambda x: datetime.datetime.strptime(x,
				 '%H:%M:%S').time(), p_dict['timings'][day])))
			except ValueError:
				try:
					timings.append(list(map(lambda x: datetime.datetime.strptime(x,
				 	'%H:%M').time(), p_dict['timings'][day])))
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
		cur_obj = { 'day' : day }
		cur_obj['start'] = b_t[0].isoformat().split('.')[0][:5]
		cur_obj['end'] = b_t[-1].isoformat().split('.')[0][:5]
		break_timings.append(cur_obj)


	return render(request, 'clinician/dashboard/timings/breaktime.html.j2', context={
		'title' : "Timings -  break",
		'clinician' : c,
		'timings' : break_timings
		})


@match_role("clinician")
def timing_vacation(request):
	''' vacations dates routes for clinician '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	if request.method == "POST":
		p_dict = parser.parse(request.POST.urlencode())
		try:
			vacs = p_dict['timings'][""]
			vacs = [ list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
			 [i, j])) for i, j in zip(vacs[::2], vacs[1::2])]
			c.vacations = vacs
			c.save()
		except:
			pass

	vacation_timings = []
	for vacation in c.vacations:
		vacation_timings.append({
			'start' : vacation[0].isoformat(),
			'end' : vacation[-1].isoformat(),
		})

	return render(request, 'clinician/dashboard/timings/vacationtime.html.j2', context={
		'title' : "Timings -  vacation",
		'clinician' : c,
		'timings' : vacation_timings,
		})

# account routes

@match_role("clinician")
def basic_details(request):
	''' account route for '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	class UserForm(forms.ModelForm):
		language_choices = (
			('english', 'english'),
			('hindi', 'hindi'),
			('telugu', 'telugu'),
			('marathi', 'marathi'),
			('malayalam', 'malayalam'),
			('gujarati', 'gujarati'),
			('bhojpuri', 'bhojpuri'),
			('tamil', 'tamil'),
			('other', 'other'),
    	)
		language = forms.ChoiceField(choices=language_choices)

		class Meta:
			model = User
			fields = ('name', 'gender', 'language',)

	if request.method == "POST":
		b = UserForm(request.POST, instance=c.user)
		if b.is_valid():
			c.language = b.cleaned_data.get('language')
			del b.__dict__['fields']['language']
			b.save()
			c.save()

	return render(request, 'clinician/dashboard/account/basic.html.j2', context={
		'title' : "Account - Basic Details",
		'clinician' : c,
		'form' : UserForm(instance=c.user, initial={'language' : c.language }),
		})


@match_role("clinician")
def professional_info(request):
	c = Clinician.objects.filter(user__email=request.session['email']).first()

	if request.method == "POST":
		ids = parser.parse(request.POST.urlencode())
		cur_specs = c.specialities.all()
		ids = ids['ids']['']
		new_specs = Speciality.objects.filter(id__in=ids)
		[c.specialities.remove(_) for _ in cur_specs if _ not in new_specs]
		[c.specialities.add(_) for _ in new_specs if _ not in cur_specs]

	cur_specs = c.specialities.all()
	all_specs = Speciality.objects.filter(id__in=Provider.objects.filter(
		clinicians__in=[c]).values_list(
			'specialities', flat=True))

	return render(request, 'clinician/dashboard/account/professionaldetails.html.j2', context={
	 	"title": "Account - Specialities",
		'specialities' : cur_specs,
		'all_specs' : all_specs,
	})



@match_role("clinician")
def education(request):
	''' account route for '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	class EducationForm(forms.Form):
		type_choices = (
			('post-graduate','post-graduate'),
			('high-school','high-school'),
			('undergraduate','undergraduate'),
			('masters','masters'),
			('other','other'),
		)
		year = forms.CharField(min_length=4, max_length=4)
		title = forms.CharField(max_length=30)
		description = forms.CharField(max_length=100, widget=forms.widgets.Textarea())
		type = forms.ChoiceField(choices=type_choices)

	edu_form = EducationForm()

	if request.method == "POST":
		if request.POST['btn-type'] == "1":
			edu_form = EducationForm(request.POST, request.FILES)
			if edu_form.is_valid():
				e = edu_form.cleaned_data
				c.education.append(e)
		elif request.POST['btn-type'] == "0":
			post_params = parser.parse(request.POST.urlencode())
			fields = ['year', 'title', 'type', 'description']
			cur_all = []
			if any([_ in post_params for _ in fields]):
				for _ in fields:
					if not isinstance(post_params[_], list):
						post_params[_] = [post_params[_]]
				cur_all = zip(post_params[fields[0]])
				for field in fields[1:]:
					cur_all = zip(*cur_all)
					cur_all = zip(*cur_all, post_params[field])
				cur_all = list(cur_all)
			records = []
			for r in cur_all:
				x = {}
				[x.update({j : i}) for i, j in zip(r, fields)]
				records.append(x)
			c.education = records

		c.save()

	edu_records = c.education
	return render(request, 'clinician/dashboard/account/education.html.j2', context={
		'title' : "Account - Education & Training",
		'clinician' : c,
		'education' : edu_form,
		'edu_records' : edu_records,
		})


@match_role("clinician")
def fee_offerings(request):
	''' account route for '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	if request.method == "POST":
		c.first_fee = request.POST['first_time']
		c.fee = request.POST['fee']
		post_params = parser.parse(request.POST.urlencode())
		fields = ['amount', 'name', 'type', 'description']
		cur_all = []
		if any([_ in post_params for _ in fields]):
			for _ in fields:
				if not isinstance(post_params[_], list):
					post_params[_] = [post_params[_]]
			cur_all = zip(post_params[fields[0]])
			for field in fields[1:]:
				cur_all = zip(*cur_all)
				cur_all = zip(*cur_all, post_params[field])
			cur_all = list(cur_all)
		records = []
		for r in cur_all:
			x = {}
			[x.update({j : i}) for i, j in zip(r, fields)]
			records.append(x)
		c.discount_offerings = records
		c.save()

	fees = c.discount_offerings
	return render(request, 'clinician/dashboard/account/consultation.html.j2', context={
		'title' : "Account - Fees",
		'clinician' : c,
		'fees' : fees,
		})


@match_role("clinician")
def condition_procedures(request):
	''' account route for '''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	class ProcedureForm(forms.Form):
		type_choices = (
			('procedure','procedure'),
			('condition','condition'),
			('other','other'),
		)

		def clean(self):
			cleaned_data = super().clean()
			cleaned_data['date'] = cleaned_data['date'].isoformat()
			return cleaned_data

		date = forms.DateField(required=False)
		name = forms.CharField(max_length=30)
		description = forms.CharField(max_length=100, widget=forms.widgets.Textarea())
		type = forms.ChoiceField(choices=type_choices)

	procedure_form = ProcedureForm()

	if request.method == "POST":
		if request.POST['btn-type'] == "1":
			procedure_form = ProcedureForm(request.POST, request.FILES)
			if procedure_form.is_valid():
				e = procedure_form.cleaned_data
				c.procedure_conditions.append(e)
				procedure_form = ProcedureForm()

		elif request.POST['btn-type'] == "0":
			post_params = parser.parse(request.POST.urlencode())
			fields = ['name', 'description', 'type', 'date']
			cur_all = []
			if any([_ in post_params for _ in fields]):
				for _ in fields:
					if not isinstance(post_params[_], list):
						post_params[_] = [post_params[_]]
				cur_all = zip(post_params[fields[0]])
				for field in fields[1:]:
					cur_all = zip(*cur_all)
					cur_all = zip(*cur_all, post_params[field])
				cur_all = list(cur_all)
			records = []
			for r in cur_all:
				x = {}
				[x.update({j : i}) for i, j in zip(r, fields)]
				records.append(x)

			print(records)
			c.procedure_conditions = records

		c.save()

	return render(request, 'clinician/dashboard/account/conditions.html.j2', context={
		'title' : "Account - Procedures/Conditions",
		'clinician' : c,
		'all_procs' : c.procedure_conditions,
		'procedure_form' : procedure_form,
		})


@match_role("clinician")
def experience_training(request):
	''' account route for experience and training'''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	class ExperienceForm(forms.Form):
		type_choices = (
			('experience','experience'),
			('training','training'),
			('other','other'),
		)

		year = forms.CharField(required=False)
		position = forms.CharField(max_length=30)
		description = forms.CharField(max_length=100, widget=forms.widgets.Textarea())
		type = forms.ChoiceField(choices=type_choices)

	experience_form = ExperienceForm()

	if request.method == "POST":
		if request.POST['btn-type'] == "1":
			experience_form = ExperienceForm(request.POST, request.FILES)
			if experience_form.is_valid():
				e = experience_form.cleaned_data
				c.experience_training.append(e)
				experience_form = ExperienceForm()

		elif request.POST['btn-type'] == "0":
			post_params = parser.parse(request.POST.urlencode())
			fields = ['year', 'position', 'description', 'type']
			cur_all = []
			if any([_ in post_params for _ in fields]):
				for _ in fields:
					if not isinstance(post_params[_], list):
						post_params[_] = [post_params[_]]
				cur_all = zip(post_params[fields[0]])
				for field in fields[1:]:
					cur_all = zip(*cur_all)
					cur_all = zip(*cur_all, post_params[field])
				cur_all = list(cur_all)
			records = []
			for r in cur_all:
				x = {}
				[x.update({j : i}) for i, j in zip(r, fields)]
				records.append(x)

			print(records)
			c.experience_training = records

		c.save()


	return render(request, 'clinician/dashboard/account/experience.html.j2', context={
		'title' : "Account - Experience & Training",
		'clinician' : c,
		'all_exp': c.experience_training,
		'experience_form' : experience_form,
		})


@match_role("clinician")
def awards_recognition(request):
	''' account route for awards and recognitions'''
	c = Clinician.objects.filter(user__email=request.session['email']).first()

	class AwardForm(forms.Form):
		name = forms.CharField()
		description = forms.CharField(max_length=100, widget=forms.widgets.Textarea())
		year = forms.CharField()
		recognised_by = forms.CharField()

	award_form = AwardForm()
	if request.method == "POST":
		if request.POST['btn-type'] == "1":
			award_form = AwardForm(request.POST, request.FILES)
			if award_form.is_valid():
				e = award_form.cleaned_data
				c.awards.append(e)
				award_form = AwardForm()

		elif request.POST['btn-type'] == "0":
			post_params = parser.parse(request.POST.urlencode())
			fields = ['name', 'description', 'year', 'recognised_by']
			cur_all = []
			if any([_ in post_params for _ in fields]):
				for _ in fields:
					if not isinstance(post_params[_], list):
						post_params[_] = [post_params[_]]
				cur_all = zip(post_params[fields[0]])
				for field in fields[1:]:
					cur_all = zip(*cur_all)
					cur_all = zip(*cur_all, post_params[field])
				cur_all = list(cur_all)
			records = []
			for r in cur_all:
				x = {}
				[x.update({j : i}) for i, j in zip(r, fields)]
				records.append(x)

			print(records)
			c.awards = records
		c.save()
	return render(request, 'clinician/dashboard/account/awards.html.j2', context={
		'title' : "Account - Awards & Recognition",
		'clinician' : c,
		'award_form' : award_form,
		'awards' : c.awards,
		})


@match_role("clinician")
def registrations(request):
	''' account route for registrations'''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	class RegistrationForm(forms.Form):
		name = forms.CharField()
		year = forms.CharField()
		reg_no = forms.CharField()

	registration_form = RegistrationForm()
	if request.method == "POST":
		if request.POST['btn-type'] == "1":
			registration_form = RegistrationForm(request.POST, request.FILES)
			if registration_form.is_valid():
				e = registration_form.cleaned_data
				c.registrations.append(e)
				registration_form = RegistrationForm()

		elif request.POST['btn-type'] == "0":
			post_params = parser.parse(request.POST.urlencode())
			fields = ['name', 'year', 'reg_no']
			cur_all = []
			if any([_ in post_params for _ in fields]):
				for _ in fields:
					if not isinstance(post_params[_], list):
						post_params[_] = [post_params[_]]
				cur_all = zip(post_params[fields[0]])
				for field in fields[1:]:
					cur_all = zip(*cur_all)
					cur_all = zip(*cur_all, post_params[field])
				cur_all = list(cur_all)
			records = []
			for r in cur_all:
				x = {}
				[x.update({j : i}) for i, j in zip(r, fields)]
				records.append(x)

			print(records)
			c.registrations = records
		c.save()

	return render(request, 'clinician/dashboard/account/registration.html.j2', context={
		'title' : "Account - Registrations",
		'clinician' : c,
		'registration_form' : registration_form,
		'registrations': c.registrations,
		})


@match_role("clinician")
def memberships(request):
	''' account route for memberships'''

	c = Clinician.objects.filter(user__email=request.session['email']).first()

	class MembershipForm(forms.Form):
		name = forms.CharField()
		country = forms.CharField()
		city = forms.CharField()

	membership_form = MembershipForm()
	if request.method == "POST":
		if request.POST['btn-type'] == "1":
			membership_form = MembershipForm(request.POST, request.FILES)
			if membership_form.is_valid():
				e = membership_form.cleaned_data
				c.memberships.append(e)
				membership_form = MembershipForm()

		elif request.POST['btn-type'] == "0":
			post_params = parser.parse(request.POST.urlencode())
			fields = ['name','country', 'city']
			cur_all = []
			if any([_ in post_params for _ in fields]):


				for _ in fields:
					if not isinstance(post_params[_], list):
						post_params[_] = [post_params[_]]
				cur_all = zip(post_params[fields[0]])
				for field in fields[1:]:
					cur_all = zip(*cur_all)
				cur_all = zip(*cur_all, post_params[field])
			cur_all = list(cur_all)
			records = []
			for r in cur_all:
				x = {}
				[x.update({j : i}) for i, j in zip(r, fields)]
				records.append(x)

			print(records)
			c.memberships = records
		c.save()

	return render(request, 'clinician/dashboard/account/memberships.html.j2', context={
		'title' : "Account - Memberships",
		'clinician' : c,
		'membership_form' : membership_form,
		'memberships' : c.memberships,
		})
