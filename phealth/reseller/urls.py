from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "reseller"

dashboard_routes = [
]

urlpatterns = [
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

