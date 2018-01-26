from django.urls import path
from django.conf.urls import url

from clinician import views

urlpatterns = [
	url(r'^signup', views.SignUp)
]
