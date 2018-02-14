from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "common"

payment_routes = [
	url(r'^$', views.payment_init, name='payment_init'),
	url(r'^success/?$', views.payment_success, name='payment_success'),
	url(r'^failure/?$', views.payment_failure, name='payment_failure'),
]

urlpatterns = [
	url(r'^signout/?$', views.logout, name='signout'),
	url(r'^payment/', include(payment_routes)),
	url(r'^otp/?$', views.send_OTP, name='otp'),
]
