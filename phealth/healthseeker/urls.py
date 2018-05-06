from django.conf.urls import include, url
from django.urls import include, path

from . import views
from .views import *

app_name = "healthseeker"

profile_routes = [

    url(r'^information/?$', views.information, name='information'),

    url(r'^family/?$', views.family, name='family'),
    url(r'^family_edit/(?P<pk>\d+)/family_edit/$', views.family_edit, name='family_edit'),
    url(r'^family_delete/family_delete/(?P<pk>\d+)/$', views.family_delete, name='family_delete'),

    path('change_password/', views.change_password, name='change_password'),
    url(r'^contact/?$', views.contact, name='contact'),
    url(r'^interests/?$', views.interests, name='intrest'),
    url(r'^other/?$', views.other, name='other'),
]

appointment_routes = [

    path('scheduled/', views.appointment_scheduled, name='appointment_scheduled'),
    path('booked/', views.appointment_booked, name='appointment_booked'),
    path('past/', views.appointment_past, name='appointment_past'),

    url(r'^complaints/?$', views.complaints, name='complaints'),
    url(r'^records/?$', views.records, name='records'),
]


dashboard_routes = [

    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^profile/', include(profile_routes)),
    url(r'^appointment/', include(appointment_routes)),

    url(r'^favourite_doctors/?$', views.favourite_doctors, name='favaroitedoctors'),
    url(r'^healthalerts/?$', views.healthalerts, name='healthalerts'),
    url(r'^reference/?$', views.reference, name='reference'),
    url(r'^accountmanager/?$', views.accountmanager, name='accountmanager'),
]

urlpatterns = [
    url(r'^signin/?$', SignIn, name='signin'),

    url(r'^registration/$',registration,name="healthseekerregistration"),

    url(r'^otp/$',otp,name="otp"),
    url(r'^step2/$',step2,name="step2"),
    url(r'^step3/$',step3,name="step3"),
    url(r'^step4/$',step4,name="step4"),
    url(r'^step5/$', step5, name="step5"),
    url(r'^step6/$', step6, name="step6"),

    url(r'^dashboard/', include(dashboard_routes)),

]

