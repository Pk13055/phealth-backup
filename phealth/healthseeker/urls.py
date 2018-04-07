from django.conf.urls import url
from .views import *
from django.urls import path, include
from django.conf.urls import include, url
from .views import *


app_name = "healthseeker"
urlpatterns = [
    url(r'^$',healthseekersignin,name="healthseekersignin"),
    url(r'^registration/?$',registration,name="healthseekerregistration"),
    url(r'^form2/?$',registrationform2,name="form2"),
    url(r'^form3/?$',registrationform3,name="form3"),
    url(r'^form4/?$', registrationform4, name="form4"),
    url(r'^form5/?$', registrationform3, name="form5"),
    url(r'^/dashboard/?$',healthseekerdashboard,name="healthseekerdashboard_home"),
    url(r'^/addfamilymembers/?$',addfamilymembers,name="addfamilymembers"),
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