from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "common"

urlpatterns = [
	url(r'^signout/?$', views.logout, name='signout'),
]
