from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "clinician"

dashboard_routes = [

	# personal
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'calender/?$', views.calender, name='calender'),
	url(r'speciality/?$', views.speciality, name='speciality'),
	url(r'appointments/?$', views.appointments, name='appointments'),


]

urlpatterns = [
    # url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes))
]
