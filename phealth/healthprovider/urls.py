from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "healthprovider"

dashboard_routes = [
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'^contact_details/?$', views.contact_details, name='contact_details'),
	# url(r'^branches/?$', views.branches, name='branches'),
	url(r'^specialities/?$', views.specialities, name='specialities'),
	url(r'^facilities/?$', views.facilities, name='facilities'),
	# url(r'^offerings/?$', views.offerings, name='offerings'),
	# url(r'^special_health_checks/?$', views.special_health_checks, name='special_health_checks'),
	# url(r'^plans/?$', views.plans, name='plans'),
	url(r'^doctors_list/?$', views.doctors_list, name='doctors_list'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

