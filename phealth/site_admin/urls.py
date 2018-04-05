from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "site_admin"

appointment_routes = [
    url(r'^daily/?$', views.AppointmentTableView.as_view(), name='appointment_daily'),
    url(r'^weekly/?$', views.appointment_weekly, name='appointment_weekly'),
    url(r'^monthly/?$', views.appointment_monthly, name='appointment_monthly'),
    path('confirm/<int:id>/', views.confirm_appointment, name='confirm_appointment'),
    path('cancel/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
]

timing_routes = [
    url(r'^work/?$', views.timing_work, name='timing_work'),
    url(r'^break/?$', views.timing_break, name='timing_break'),
    url(r'^vacation/?$', views.timing_vacation, name='timing_vacation'),
]

account_routes = [
    url(r'^basic_details/?$', views.basic_details, name='basic_details'),
    url(r'^professional_info/?$', views.professional_info, name='professional_info'),
    url(r'^education_training/?$', views.education_training, name='education_training'),
    url(r'^consultation_fee/?$', views.consultation_fee, name='consultation_fee'),
    url(r'^offerings/?$', views.offerings, name='offerings'),
    url(r'^conditions_treated/?$', views.conditions_treated, name='conditions_treated'),
    url(r'^procedures/?$', views.procedures, name='procedures'),
    url(r'^experience/?$', views.experience, name='experience'),
    url(r'^awards_recognition/?$', views.awards_recognition, name='awards_recognition'),
    url(r'^registrations/?$', views.registrations, name='registrations'),
    url(r'^memberships/?$', views.memberships, name='memberships'),
]

dashboard_routes = [

    url(r'^cms_add/?$', views.cms_add, name='cms_add'),
    url(r'^cms_view/?$', views.cms_view, name='cms_view'),
    url(r'^condition_add/?$', views.condition_add, name='condition_add'),
    url(r'^condition_view/?$', views.ConditionTableView.as_view(), name='condition_view'),
    url(r'^condition_edit/(?P<pk>\d+)/condition_edit/$', views.condition_edit, name='condition_edit'),
    url(r'^condition_delete/condition_delete/(?P<pk>\d+)/$', views.condition_delete, name='condition_delete'),

    url(r'^symptomsarea_add/?$', views.symptomsarea_add, name='symptomsarea_add'),
    url(r'^symptomsarea_view/?$', views.ConditionTableView.as_view(), name='symptomsarea_view'),
    url(r'^symptomsarea_edit/(?P<pk>\d+)/symptomsarea_edit/$', views.symptomsarea_edit, name='symptomsarea_edit'),
    url(r'^symptomsarea_delete/symptomsarea_delete/(?P<pk>\d+)/$', views.symptomsarea_delete, name='symptomsarea_delete'),



    url(r'^coupons_add/?$', views.coupons_add, name='coupons_add'),
    url(r'^coupons_view/?$', views.coupons_view, name='coupons_view'),
    url(r'^coupons_edit/(?P<pk>\d+)/coupons_edit/$', views.coupons_edit, name='coupons_edit'),
    url(r'^coupons_delete/coupons_delete/(?P<pk>\d+)/$', views.coupons_delete, name='coupons_delete'),
    url(r'^coupons_reports/?$', views.coupons_reports, name='coupons_reports'),

    url(r'^facility_type_add/?$', views.facility_type_add, name='facility_type_add'),
    url(r'^facility_type_view/?$', views.facility_type_view, name='facility_type_view'),
    url(r'^facility_type_edit/(?P<pk>\d+)/facility_type_edit/$', views.facility_type_edit, name='facility_type_edit'),
    url(r'^facility_type_delete/facility_type_delete/(?P<pk>\d+)/$', views.facility_type_delete,
        name='facility_type_delete'),

    url(r'^facility_add/?$', views.facility_add, name='facility_add'),
    url(r'^facility_view/?$', views.facility_view, name='facility_view'),
    url(r'^facility_edit/(?P<pk>\d+)/facility_edit/$', views.facility_edit, name='facility_edit'),
    url(r'^facility_delete/facility_delete/(?P<pk>\d+)/$', views.facility_delete, name='facility_delete'),

    url(r'^timesession_add/?$', views.timesession_add, name='timesession_add'),
    url(r'^timesession_view/?$', views.timesession_view, name='timesession_view'),
    url(r'^speciality_add/?$', views.speciality_add, name='speciality_add'),
    url(r'^speciality_view/?$', views.speciality_view, name='speciality_view'),

    url(r'^speciality_edit/(?P<pk>\d+)/speciality_edit/$', views.speciality_edit, name='speciality_edit'),
    url(r'^speciality_delete/speciality_delete/(?P<pk>\d+)/$', views.speciality_delete, name='speciality_delete'),
    url(r'^coupons_add/?$', views.coupons_add, name='coupons_add'),
    url(r'^coupons_view/?$', views.coupons_view, name='coupons_view'),
    url(r'^coupons_reports/?$', views.coupons_reports, name='coupons_reports'),

    url(r'^test_add/?$', views.test_add, name='test_add'),
    url(r'^test_view/?$', views.test_view, name='test_view'),
    url(r'^test_edit/(?P<pk>\d+)/test_edit/$', views.test_edit, name='test_edit'),
    url(r'^test_delete/test_delete/(?P<pk>\d+)/$', views.test_delete, name='test_delete'),
    url(r'^test_category_add/?$', views.test_category_add, name='test_category_add'),
    url(r'^test_category_view/?$', views.test_category_view, name='test_category_view'),
    url(r'^test_category_edit/(?P<pk>\d+)/test_category_edit/$', views.test_category_edit, name='test_category_edit'),
    url(r'^test_category_delete/tetest_category_delete/(?P<pk>\d+)/$', views.test_category_delete,
        name='test_category_delete'),
    url(r'^test_subcategory_add/?$', views.test_subcategory_add, name='test_subcategory_add'),
    url(r'^test_subcategory_view/?$', views.test_subcategory_view, name='test_subcategory_view'),

    url(r'^test_subcategory_edit/(?P<pk>\d+)/test_subcategory_edit/$', views.test_subcategory_edit,
        name='test_subcategory_edit'),
    url(r'^test_subcategory_delete/tetest_subcategory_delete/(?P<pk>\d+)/$', views.test_subcategory_delete,
        name='test_subcategory_delete'),
    url(r'^facility_type_add/?$', views.facility_type_add, name='facility_type_add'),
    url(r'^facility_type_view/?$', views.facility_type_view, name='facility_type_view'),
    url(r'^facility_add/?$', views.facility_add, name='facility_add'),
    url(r'^facility_view/?$', views.facility_view, name='facility_view'),

    url(r'^roles_add/?$', views.roles_add, name='roles_add'),
    url(r'^roles_view/?$', views.roles_view, name='roles_view'),
    url(r'^idconfiguration_add/?$', views.idconfiguration_add, name='idconfiguration_add'),
    url(r'^idconfiguration_view/?$', views.idconfiguration_view, name='idconfiguration_view'),
    url(r'^users/?$', views.users, name='users'),
    url(r'^salesagents_add/?$', views.salesagents_add, name='salesagents_add'),
    url(r'^salesagents_view/?$', views.salesagents_view, name='salesagents_view'),
    url(r'^health_daily/?$', views.health_daily, name='health_daily'),
    url(r'^health_weekly/?$', views.health_weekly, name='health_weekly'),
    url(r'^health_monthly/?$', views.health_monthly, name='health_monthly'),
    url(r'^discountcard_add/?$', views.discountcard_add, name='discountcard_add'),
    url(r'^discountcard_view/?$', views.discountcard_view, name='discountcard_view'),
    url(r'^discountcard_reports/?$', views.discountcard_reports, name='discountcard_reports'),
    url(r'^discountcard_edit/(?P<pk>\d+)/discountcard_edit/$', views.discountcard_edit, name='discountcard_edit'),
    url(r'^discountcard_delete/discountcard_delete/(?P<pk>\d+)/$', views.dicountcard_delete,
        name='discountcard_delete'),
    url(r'^healthcheck_add/?$', views.healthcheck_add, name='healthcheck_add'),
    url(r'^healthcheck_view/?$', views.healthcheck_view, name='healthcheck_view'),
    url(r'^healthcheck_edit/(?P<pk>\d+)/healthcheck_edit/$', views.healthcheck_edit, name='healthcheck_edit'),
    url(r'^healthcheck_delete/healthcheck_delete/(?P<pk>\d+)/$', views.dicountcard_delete, name='healthcheck_delete'),
    url(r'^healthcheck_reports/?$', views.healthcheck_reports, name='healthcheck_reports'),
    url(r'^healthprovider_plans_add/?$', views.healthprovider_plans_add, name='healthprovider_plans_add'),
    url(r'^healthprovider_plans_view/?$', views.healthprovider_plans_view, name='healthprovider_plans_view'),
    url(r'^healthprovider_plans_reports/?$', views.healthprovider_plans_reports, name='healthprovider_plans_reports'),
    url(r'^salesagents_packages_add/?$', views.salesagents_packages_add, name='salesagents_packages_add'),
    url(r'^salesagents_packages_view/?$', views.salesagents_packages_view, name='salesagents_packages_view'),
    url(r'^salesagents_packages_reports/?$', views.salesagents_packages_reports, name='salesagents_packages_reports'),
    url(r'^resellers_packages_add/?$', views.resellers_packages_add, name='resellers_packages_add'),
    url(r'^resellers_packages_view/?$', views.resellers_packages_view, name='resellers_packages_view'),
    url(r'^resellers_packages_reports/?$', views.resellers_packages_reports, name='resellers_packages_reports'),

    # old_routes
    # url(r'^$', views.dashboard, name='dashboard_home'),
    # url(r'calender/?$', views.calender, name='calender'),
    # url(r'speciality/?$', views.speciality, name='speciality'),
    # url(r'appointments/?$', views.appointments, name='appointments'),

    # new routes
    url(r'^$', views.new_home, name='dashboard_home_new'),  # remove new later
    url(r'^appointments/', include(appointment_routes)),
    url(r'^timings/', include(timing_routes)),
    url(r'account/', include(account_routes)),

]

urlpatterns = [
    # url(r'^signup/?$', views.SignUp, name='signup'),

    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
    url(r'^signup/?$', views.SignUp, name='signup'),
]



