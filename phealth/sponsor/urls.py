from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "sponsor"

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin')
]
