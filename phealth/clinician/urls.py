from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "clinician"

appointment_routes = [
	url(r'^daily/?$', views.AppointmentTableView.as_view(), name='appointment_daily'),
	url(r'^weekly/?$', views.appointment_weekly, name='appointment_weekly'),
	url(r'^monthly/?$', views.appointment_monthly, name='appointment_monthly'),
	
	path('confirm/<int:id>/', views.confirm_appointment, name='confirm_appointment'),
	path('cancel/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
]

timing_routes = [
	url(r'^work/?$', views.timing_work, name='timing_work'),
	url(r'^break/?$', views.timing_break, name='timing_break'),
	url(r'^vacation/?$', views.timing_vacation, name='timing_vacation'),
]

account_routes = [
	url(r'^basic_details/?$', views.basic_details, name='basic_details'),
	url(r'^professional_info/?$', views.professional_info, name='professional_info'),
	url(r'^education_training/?$', views.education_training, name='education_training'),
	url(r'^consultation_fee/?$', views.consultation_fee, name='consultation_fee'),
	url(r'^offerings/?$', views.offerings, name='offerings'),
	url(r'^conditions_treated/?$', views.conditions_treated, name='conditions_treated'),
	url(r'^procedures/?$', views.procedures, name='procedures'),
	url(r'^experience/?$', views.experience, name='experience'),
	url(r'^awards_recognition/?$', views.awards_recognition, name='awards_recognition'),
	url(r'^registrations/?$', views.registrations, name='registrations'),
	url(r'^memberships/?$', views.memberships, name='memberships'),
]

dashboard_routes = [

	# old_routes
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'calender/?$', views.calender, name='calender'),
	url(r'speciality/?$', views.speciality, name='speciality'),
	url(r'appointments/?$', views.appointments, name='appointments'),

	# new routes
	url(r'^home/?$', views.new_home, name='dashboard_home_new'), # remove new later
	url(r'^appointments/', include(appointment_routes)),
	url(r'^timings/', include(timing_routes)),
	url(r'account/', include(account_routes)),

]

urlpatterns = [
    # url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
    url(r'^signup/?$', views.SignUp, name='signup'),
]
