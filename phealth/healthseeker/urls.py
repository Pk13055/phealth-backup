from django.conf.urls import url
from .views import *
from django.urls import path, include
from django.conf.urls import include, url
from .views import *
from . import views



app_name = "healthseeker"
urlpatterns = [
    url(r'^$',healthseekersignin,name="healthseekersignin"),
    url(r'^registration/$',registration,name="healthseekerregistration"),
    url(r'^form2/$',registrationform2,name="form2"),
    url(r'^form3/$',registrationform3,name="form3"),
    url(r'^form3_edit/(?P<pk>\d+)/form3_edit/$', views.registrationform3, name='form3_edit'),
    url(r'^form3_delete/form3_delete/(?P<pk>\d+)/$', views.registrationform3, name='form3_delete'),
    url(r'^/dashboard/$',healthseekerdashboard,name="healthseekerdashboard_home"),
    url(r'^/addfamilymembers/$',addfamilymembers,name="addfamilymembers"),
    url(r'^accountmanager/?$', accountmanager, name='accountmanager'),
    url(r'^contactdetails/?$', contactdetails, name='contactdetails'),
    url(r'^intrest/?$', intrest, name='intrest'),
    url(r'^booking/?$', booking, name='booking'),
    url(r'^favaroitedoctors/?$', favaroitedoctors, name='favaroitedoctors'),
    url(r'^complaints/?$', complaints, name='complaints'),
    url(r'^healthalerts/?$', healthalerts, name='healthalerts'),

]