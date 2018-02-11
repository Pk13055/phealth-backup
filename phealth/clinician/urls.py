from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "clinician"

dashboard_routes = [

	# personal
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'education_training/?$', views.education_training, name='education'),

	# professional
	url(r'calendar/?$', views.calender, name='calender'),
	url(r'surgeries/?$', views.surgeries, name='surgeries'),
	url(r'conditions/?$', views.conditions, name='conditions'),
	url(r'membership/?$', views.membership, name='membership'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes))
]
