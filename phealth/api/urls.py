from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "api"

custom_apis = [

	path('doctors/', views.doctors_list, name='doctors_list'),

	path('healthchecks/<uuid:healthcheck>/', views.healthchecks_list, name='healthchecks_list'),
	path('healthchecks/', views.healthchecks_list, name='healthchecks_list'),
	
	path('healthcheck/providers/', views.location_providers, name='location_providers'),


	path('appointment/<uuid:appointment_uid>/', views.get_appointment, name='get_appointment'),
	path('appointment/', views.make_appointment, name='book_appointment'),
	path('attach_user/', views.attach_user, name='attach_user')

]

urlpatterns = [
	url(r'^custom/', include(custom_apis)),
]

router = DefaultRouter()

router.register(r'coupon', views.CouponViewSet)
router.register(r'testcategory', views.TestCategoryViewSet)
router.register(r'testsubcategory', views.TestSubcategoryViewSet)
router.register(r'symptoms', views.SymptomViewSet)
router.register(r'test', views.TestViewSet)
router.register(r'healthcheckup', views.HealthCheckupViewSet)
router.register(r'discountcard', views.DiscountCardViewSet)
router.register(r'speciality', views.SpecialityViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'transaction', views.TransactionViewSet)
router.register(r'seeker', views.SeekerViewSet)
router.register(r'clinician', views.ClinicianViewSet)
router.register(r'provider', views.ProviderViewSet)
router.register(r'sponsor', views.SponsorViewSet)
router.register(r'reseller', views.ResellerViewSet)
router.register(r'salesagent', views.SalesAgentViewSet)
router.register(r'appointment', views.AppointmentViewSet)
router.register(r'testimonial', views.TestimonialViewSet)
router.register(r'cdn', views.CDNViewSet)
router.register(r'blogcategory', views.BlogCategoryViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'blogcomment', views.BlogCommentViewSet)

urlpatterns += router.urls
