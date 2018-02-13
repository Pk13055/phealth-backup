from rest_framework.routers import DefaultRouter
from api import views

app_name = "api"

router = DefaultRouter()

router.register(r'country', views.CountryViewSet)
router.register(r'state', views.StateViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'district', views.DistrictViewSet)
router.register(r'address', views.AddressViewSet)
router.register(r'coupon', views.CouponViewSet)
router.register(r'testcategory', views.TestCategoryViewSet)
router.register(r'testsubcategory', views.TestSubcategoryViewSet)
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

urlpatterns = router.urls
