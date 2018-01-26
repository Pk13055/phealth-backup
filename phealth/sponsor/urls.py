from django.urls import path, include
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^signup/', views.SignUp),
]
