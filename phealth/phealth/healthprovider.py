from django.urls import path
from django.conf.urls import url

from healthprovider import views

urlpatterns = [
	url(r'^signup', views.SignUp)
]
