from django.conf.urls import url
from .views import healthseekersignin, healthseekerdashboard, registration,registrationform2,registrationform3,addfamilymembers


app_name = "healthseeker"
urlpatterns = [
    url(r'^$',healthseekersignin,name="healthseekersignin"),
    url(r'^registration/$',registration,name="healthseekerregistration"),
    url(r'^form2/$',registrationform2,name="form2"),
    url(r'^form3/$',registrationform3,name="form3"),
    url(r'^/dashboard/$',healthseekerdashboard,name="healthseekerdashboard_home"),
    url(r'^/addfamilymembers/$',addfamilymembers,name="addfamilymembers")
]