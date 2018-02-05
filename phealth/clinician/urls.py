from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "clinician"

dashboard_routes = [
	url(r'calender/?$', views.calender, name='calender'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes))
]
