from django.conf.urls import url
from .views import *
from django.urls import path, include
from django.conf.urls import include
from .views import *
from . import views



app_name = "healthseeker"
urlpatterns = [
    url(r'^$',healthseekersignin,name="healthseekersignin"),
    url(r'^registration/$',registration,name="healthseekerregistration"),
    url(r'^otp/$',otp,name="otp"),
    url(r'^step2/$',step2,name="step2"),
    url(r'^step3/$',step3,name="step3"),
    url(r'^step4/$',step4,name="step4"),
    url(r'^step5/$', registrationform5, name="step5"),
    url(r'^family_edit/(?P<pk>\d+)/family_edit/$', views.family_edit, name='family_edit'),
    url(r'^family_delete/family_delete/(?P<pk>\d+)/$', views.family_delete, name='family_delete'),
    url(r'^dashboard/$',healthseekerdashboard,name="healthseekerdashboard_home"),
    url(r'^addfamilymembers/$',addfamilymembers,name="addfamilymembers"),

    url(r'^signin/?$', SignIn, name='signin'),

    url(r'^accountmanager/?$', accountmanager, name='accountmanager'),
    url(r'^contactdetails/?$', contactdetails, name='contactdetails'),
    url(r'^intrest/?$', intrest, name='intrest'),
    url(r'^booking/?$', booking, name='booking'),
    url(r'^favaroitedoctors/?$', favaroitedoctors, name='favaroitedoctors'),
    url(r'^complaints/?$', complaints, name='complaints'),
    url(r'^healthalerts/?$', healthalerts, name='healthalerts'),
    url(r'^schedule/?$', schedule, name='schedule'),
    url(r'^reference/?$', reference, name='reference'),
    url(r'^information/?$', personalinformation, name='information'),
    url(r'^otherinformation/?$', otherinformation, name='otherinformation'),
    url(r'^records/?$', records, name='records'),
    url(r'^familyinformation/?$', addfamilymembers, name='familyinformation'),
    url(r'^changepassword/?$', changepassword, name='changepassword'),
]