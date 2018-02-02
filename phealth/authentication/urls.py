from django.conf.urls import include, url

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from . import views

urlpatterns = [
    url(r'^generate/?$', obtain_jwt_token),
    url(r'^refresh/?$', refresh_jwt_token),
    url(r'^verify/?$', verify_jwt_token),
    url(r'^otp/?$', views.otphandle),
]
