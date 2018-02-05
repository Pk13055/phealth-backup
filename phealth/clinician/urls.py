from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "clinician"

dashboard_routes = [
	url(r'', views.dashboard, name='dashboard'),
	url(r'personal_info/?$', views.personal_info, name='personal_info'),
	url(r'professional_info/?$', views.professional_info, name='professional_info'),
	url(r'education_training/?$', views.education_training, name='education_training'),
	url(r'consultation_fee/?$', views.consultation_fee, name='consultation_fee'),
	url(r'offerings/?$', views.offerings, name='offerings'),
	url(r'conditions_treated/?$', views.conditions_treated, name='conditions_treated'),
	url(r'experience/?$', views.experience, name='experience'),
	url(r'award_recognition/?$', views.award_recognition, name='award_recognition'),
	url(r'registrations/?$', views.registrations, name='registrations'),
	url(r'membership/?$', views.membership, name='membership'),
	url(r'areas_of_interest/?$', views.areas_of_interest, name='areas_of_interest'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes))
]
