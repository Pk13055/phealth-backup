from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "sponsor"

dashboard_urls = [
	url(r'^$', views.dashboard, name='dashboard_home'), # basic details
	url(r'^users/?$', views.user_view, name='users'), # user addition
	url(r'^discounts/?$', views.discounts, name='discounts'), # discountcard details
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_urls))
]
