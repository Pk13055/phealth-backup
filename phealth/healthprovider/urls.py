from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "healthprovider"

account_routes = [
	url(r'^basic/?$', views.account_basic, name="account_basic"),
	url(r'^contact/?$', views.account_contact, name="account_contact"),
	url(r'^speciality/?$', views.account_speciality, name="account_speciality"),
	url(r'^facilities/?$', views.account_facilities, name="account_facilities"),
	url(r'^offerings/?$', views.account_offerings, name="account_offerings"),
	url(r'^special_checks/?$', views.account_special_checks, name="account_special_checks"),
]

branch_update_routes = [
	url(r'^basic/?$', views.branch_basic, name="branch_basic_update"),
	url(r'^contact/?$', views.branch_contact, name="branch_contact_update"),
	url(r'^facilities/?$', views.branch_facilities, name="branch_facilities_update"),
	url(r'^healthcheck/?$', views.branch_healthcheck, name="branch_healthcheck_update"),
	url(r'^offerings/?$', views.branch_offerings, name="branch_offerings_update"),
	url(r'^organization/?$', views.branch_organization, name="branch_organization_update"),
	url(r'^speciality/?$', views.branch_speciality, name="branch_speciality_update"),
]

branch_routes = [
	url(r'^new/?$', views.branch_new, name="branch_new"),
	url(r'^view/?$', views.branch_view, name="branch_view"),
	url(r'^update/', include(branch_update_routes)),
]

appointment_routes = [
	url(r'^daily/?$', views.appointment_daily, name="appointment_daily"),
	url(r'^weekly/?$', views.appointment_weekly, name="appointment_weekly"),
	url(r'^monthly/?$', views.appointment_monthly, name="appointment_monthly"),
]

payment_routes = [
	url(r'^new/?$', views.payment_new, name="payment_new"),
	url(r'^add/?$', views.payment_add, name="payment_add"),
	url(r'^view/?$', views.payment_view, name="payment_view"),
]

clinician_routes = [
	url(r'^new/?$', views.clinician_new, name="clinician_new"),
	url(r'^view/?$', views.clinician_view, name="clinician_view"),
]

# dashboard routes
dashboard_routes = [
	
	# old routes
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'^branches/?$', views.branches, name='branches'),
	url(r'^specialities/?$', views.specialities, name='specialities'),
	url(r'^clinicians/?$', views.clinicians, name='clinicians'),
	url(r'^appointments/?$', views.appointments, name='appointments'),

	# new routes
	url(r'^home/?$', views.dashboard_home, name='dashboard_home_new'),
	url(r'^account/', include(account_routes)),
	url(r'branches/', include(branch_routes)),
	url(r'appointments/', include(appointment_routes)),
	url(r'clinicians/', include(clinician_routes)),
	url(r'payments/', include(payment_routes)),
]

# actual routes
urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

