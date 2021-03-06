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
	url(r'^education/?$', views.education, name='education'),
	url(r'^fee_offerings/?$', views.fee_offerings, name='fee_offerings'),
	url(r'^condition_procedures/?$', views.condition_procedures, name='condition_procedures'),
	url(r'^experience_training/?$', views.experience_training, name='experience_training'),
	url(r'^awards_recognition/?$', views.awards_recognition, name='awards_recognition'),
	url(r'^registrations/?$', views.registrations, name='registrations'),
	url(r'^memberships/?$', views.memberships, name='memberships'),
]

dashboard_routes = [
	url(r'^$', views.new_home, name='dashboard_home'),
	url(r'^appointments/', include(appointment_routes)),
	url(r'^timings/', include(timing_routes)),
	url(r'account/', include(account_routes)),
]

urlpatterns = [
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
    url(r'^signup/?$', views.SignUp, name='signup'),
]
