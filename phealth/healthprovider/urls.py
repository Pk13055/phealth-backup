from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "healthprovider"

dashboard_routes = [
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'^branches/?$', views.branches, name='branches'),
	url(r'^specialities/?$', views.specialities, name='specialities'),
	url(r'^clinicians/?$', views.clinicians, name='clinicians'),
	url(r'^appointments/?$', views.appointments, name='appointments'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

