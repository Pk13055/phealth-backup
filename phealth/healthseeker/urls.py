from django.conf.urls import include, url
from django.urls import include, path

from . import views
from .views import *

app_name = "healthseeker"

appointment_routes = [
    path('scheduled/', views.appointment_scheduled, name='appointment_scheduled'),
    path('booked/', views.appointment_booked, name='appointment_booked'),
    path('past/', views.appointment_past, name='appointment_past'),
]

urlpatterns = [
    url(r'^$',healthseekersignin,name="healthseekersignin"),
    url(r'^registration/$',registration,name="healthseekerregistration"),
    url(r'^otp/$',otp,name="otp"),
    url(r'^form2/$',registrationform2,name="form2"),
    url(r'^step3/$',step3,name="step3"),
    url(r'^family_edit/(?P<pk>\d+)/family_edit/$', views.family_edit, name='family_edit'),
    url(r'^family_delete/family_delete/(?P<pk>\d+)/$', views.family_delete, name='family_delete'),
    url(r'^dashboard/$',healthseekerdashboard,name="healthseekerdashboard_home"),
    url(r'^addfamilymembers/$',addfamilymembers,name="addfamilymembers"),

    url(r'^signin/?$', SignIn, name='signin'),
    url(r'^appointments/', include(appointment_routes)),
    url(r'^accountmanager/?$', accountmanager, name='accountmanager'),
    url(r'^contactdetails/?$', contactdetails, name='contactdetails'),
    url(r'^intrest/?$', intrest, name='intrest'),
    url(r'^favaroitedoctors/?$', favaroitedoctors, name='favaroitedoctors'),
    url(r'^complaints/?$', complaints, name='complaints'),
    url(r'^healthalerts/?$', healthalerts, name='healthalerts'),
    url(r'^reference/?$', reference, name='reference'),
    url(r'^information/?$', personalinformation, name='information'),
    url(r'^otherinformation/?$', otherinformation, name='otherinformation'),
    url(r'^records/?$', records, name='records'),
    url(r'^familyinformation/?$', addfamilymembers, name='familyinformation'),
    url(r'^changepassword/?$', changepassword, name='changepassword'),
]
