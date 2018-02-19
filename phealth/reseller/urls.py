from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "reseller"

dashboard_routes = [
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'^discounts/?$', views.discounts, name='discounts'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

