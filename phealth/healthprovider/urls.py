from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "healthprovider"

dashboard_routes = [
	url(r'^$', views.Dashboard, name='dashboard'),
	url(r'^basic_details/?$', views.BasicDetails, name='basic_details'),
	url(r'^contact_details/?$', views.ContactDetails, name='contact_details'),
	url(r'^branches/?$', views.Branches, name='branches'),
	url(r'^specialities/?$', views.Specialities, name='specialities'),
	url(r'^facilities/?$', views.Facilities, name='facilities'),
	url(r'^offerings/?$', views.Offerings, name='offerings'),
	url(r'^special_health_checks/?$', views.SpecialHealthChecks, name='special_health_checks'),
	url(r'^plans/?$', views.Plans, name='plans'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

