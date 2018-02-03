from django.urls import path, include
from django.conf.urls import include, url

from . import views

dashboard_routes = [
	url(r'calender/?$', views.calender),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp),
    url(r'^signin/?$', views.SignIn),
    url(r'^dashboard/', include(dashboard_routes))
]
