from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "sponsor"

dashboard_urls = [
	url(r'^$', views.dashboard, name='dashboard_home'), # basic details
	url(r'^oragnization/?$', views.organization, name='dashboard_organization'), # oragnization details
	url(r'^education/?$', views.education, name='dashboard_education'), # education and training
	url(r'^contact/?$', views.contact, name='dashboard_contact'), #contact details
	url(r'^business/?$', views.business, name='dashboard_business'), #business details
	url(r'^participants/?$', views.participants, name='dashboard_participants'), #participants details
	url(r'^discounts/?$', views.discounts, name='dashboard_discount'), #discount details
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_urls))
]
