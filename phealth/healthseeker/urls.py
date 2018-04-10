from django.conf.urls import url
from .views import *
from django.urls import path, include
from django.conf.urls import include
from .views import *
from . import views



app_name = "healthseeker"

profile_routes = [
    url(r'^information/?$', views.information, name='information'),
    url(r'^family/?$', views.family, name='family'),
    url(r'^family_edit/(?P<pk>\d+)/family_edit/$', views.family_edit, name='family_edit'),
    url(r'^family_delete/family_delete/(?P<pk>\d+)/$', views.family_delete, name='family_delete'),
    url(r'^contact/?$', views.contact, name='contact'),
    url(r'^other/?$', views.other, name='other'),
]

appointment_routes = [
    url(r'^booking/?$', views.booking, name='booking'),
    url(r'^intrest/?$', views.intrest, name='intrest'),
    url(r'^favaroitedoctors/?$', views.favaroitedoctors, name='favaroitedoctors'),
    url(r'^complaints/?$', views.complaints, name='complaints'),
    url(r'^healthalerts/?$', views.healthalerts, name='healthalerts'),
    url(r'^schedule/?$', views.schedule, name='schedule'),
    url(r'^records/?$', views.records, name='records'),
    url(r'^reference/?$', views.reference, name='reference'),
    url(r'^accountmanager/?$', views.accountmanager, name='accountmanager'),
]


dashboard_routes = [
	url(r'^$', views.dashboard, name='dashboard'),
    url(r'^profile/', include(profile_routes)),
    url(r'^appointment/', include(appointment_routes)),
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

