'''
contains the router for the api routes and the like 

'''

from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()


router.register(r'address', views.AddressViewSet)
router.register(r'agegroup', views.AgegroupViewSet)
router.register(r'alertsources', views.AlertsourcesViewSet)
router.register(r'alerttype', views.AlerttypeViewSet)
router.register(r'appointmentbooking', views.AppointmentbookingViewSet)
router.register(r'availablefacilities', views.AvailablefacilitiesViewSet)
router.register(r'bookingsources', views.BookingsourcesViewSet)
router.register(r'businessregtype', views.BusinessregtypeViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'clinicianmemberships', views.ClinicianMembershipsViewSet)
router.register(r'clinicians', views.CliniciansViewSet)
router.register(r'cliniciansdates', views.CliniciansDatesViewSet)
router.register(r'clinicianseducation', views.CliniciansEducationViewSet)
router.register(r'cliniciansexperience', views.CliniciansExperienceViewSet)
router.register(r'cliniciansspeciality', views.CliniciansSpecialityViewSet)
router.register(r'conditions', views.ConditionsViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'couponaccept', views.CouponacceptViewSet)
router.register(r'coupons', views.CouponsViewSet)
router.register(r'designation', views.DesignationViewSet)
router.register(r'discountcard', views.DiscountcardViewSet)
router.register(r'discountcardfamily', views.DiscountcardFamilyViewSet)
router.register(r'discountcardfamilyextra', views.DiscountcardFamilyExtraViewSet)
router.register(r'district', views.DistrictViewSet)
router.register(r'facilities', views.FacilitiesViewSet)
router.register(r'facilitiesservices', views.FacilitiesServicesViewSet)
router.register(r'family', views.FamilyViewSet)
router.register(r'feedback', views.FeedbackViewSet)
router.register(r'gender', views.GenderViewSet)
router.register(r'healthcheckbooking', views.HealthcheckbookingViewSet)
router.register(r'healthchecks', views.HealthchecksViewSet)
router.register(r'healthchecksinclusion', views.HealthchecksInclusionViewSet)
router.register(r'healthproviders', views.HealthprovidersViewSet)
router.register(r'healthprovidersspeciality', views.HealthprovidersSpecialityViewSet)
router.register(r'healthrecords', views.HealthrecordsViewSet)
router.register(r'healthseeker', views.HealthseekerViewSet)
router.register(r'healthseekeralerts', views.HealthseekerAlertsViewSet)
router.register(r'healthseekeravailabilities', views.HealthseekerAvailabilitiesViewSet)
router.register(r'healthseekerhealthrecords', views.HealthseekerHealthrecordsViewSet)
router.register(r'healthseekertype', views.HealthseekerTypeViewSet)
router.register(r'interest', views.InterestViewSet)
router.register(r'languages', views.LanguagesViewSet)
router.register(r'photoalbum', views.PhotoalbumViewSet)
router.register(r'plans', views.PlansViewSet)
router.register(r'plansgroups', views.PlansGroupsViewSet)
router.register(r'plansgroupsspecialities', views.PlansGroupsSpecialitiesViewSet)
router.register(r'priyority', views.PriyorityViewSet)
router.register(r'profession', views.ProfessionViewSet)
router.register(r'qualification', views.QualificationViewSet)
router.register(r'referrels', views.ReferrelsViewSet)
router.register(r'referrelscheme', views.ReferrelschemeViewSet)
router.register(r'registrationwelcomemessage', views.RegistrationWelcomeMessageViewSet)
router.register(r'resellerpackages', views.ResellerpackagesViewSet)
router.register(r'resellers', views.ResellersViewSet)
router.register(r'role', views.RoleViewSet)
router.register(r'salesagentpackages', views.SalesagentpackagesViewSet)
router.register(r'salesagents', views.SalesagentsViewSet)
router.register(r'salestarget', views.SalestargetViewSet)
router.register(r'secretquestions', views.SecretquestionsViewSet)
router.register(r'speciality', views.SpecialityViewSet)
router.register(r'specialitytype', views.SpecialityTypeViewSet)
router.register(r'sponsors', views.SponsorsViewSet)
router.register(r'sponsorsgroup', views.SponsorsGroupViewSet)
router.register(r'state', views.StateViewSet)
router.register(r'symptoms', views.SymptomsViewSet)
router.register(r'telephone', views.TelephoneViewSet)
router.register(r'test', views.TestViewSet)
router.register(r'testcategory', views.TestCategoryViewSet)
router.register(r'testsubcategory', views.TestSubcategoryViewSet)
router.register(r'testimonials', views.TestimonialsViewSet)
router.register(r'timeslots', views.TimeslotsViewSet)
router.register(r'trxnappointmentbookings', views.TrxnAppointmentbookingsViewSet)
router.register(r'trxncoupons', views.TrxnCouponsViewSet)
router.register(r'trxndiscountcard', views.TrxnDiscountcardViewSet)
router.register(r'trxnhealthcheckbooking', views.TrxnHealthcheckbookingViewSet)
router.register(r'trxnpayments', views.TrxnPaymentsViewSet)
router.register(r'users', views.UsersViewSet)
router.register(r'week', views.WeekViewSet)
router.register(r'wellnessplan', views.WellnessplanViewSet)
router.register(r'wellnessplanprofession', views.WellnessplanProfessionViewSet)
router.register(r'wellnessplansocialhistory', views.WellnessplanSocialhistoryViewSet)