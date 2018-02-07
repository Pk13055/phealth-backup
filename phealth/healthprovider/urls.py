from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "healthprovider"

dashboard_routes = [
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'^contact_details/?$', views.contact_details, name='dashboard_contact_details'),
	url(r'^branches/?$', views.branches, name='dashboard_branches'),
	url(r'^specialities/?$', views.specialities, name='dashboard_specialities'),
	url(r'^facilities/?$', views.facilities, name='dashboard_facilities'),
	url(r'^offerings/?$', views.offerings, name='dashboard_offerings'),
	url(r'^special_health_checks/?$', views.special_health_checks, name='dashboard_special_health_checks'),
	url(r'^plans/?$', views.plans, name='dashboard_plans'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

