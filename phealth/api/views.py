from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from api.models import *


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AgegroupViewSet(ModelViewSet):
    queryset = Agegroup.objects.all()
    serializer_class = AgegroupSerializer


class AlertsourcesViewSet(ModelViewSet):
    queryset = Alertsources.objects.all()
    serializer_class = AlertsourcesSerializer


class AlerttypeViewSet(ModelViewSet):
    queryset = Alerttype.objects.all()
    serializer_class = AlerttypeSerializer


class AppointmentbookingViewSet(ModelViewSet):
    queryset = Appointmentbooking.objects.all()
    serializer_class = AppointmentbookingSerializer


class AvailablefacilitiesViewSet(ModelViewSet):
    queryset = Availablefacilities.objects.all()
    serializer_class = AvailablefacilitiesSerializer


class BookingsourcesViewSet(ModelViewSet):
    queryset = Bookingsources.objects.all()
    serializer_class = BookingsourcesSerializer


class BusinessregtypeViewSet(ModelViewSet):
    queryset = Businessregtype.objects.all()
    serializer_class = BusinessregtypeSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ClinicianMembershipsViewSet(ModelViewSet):
    queryset = ClinicianMemberships.objects.all()
    serializer_class = ClinicianMembershipsSerializer


class CliniciansViewSet(ModelViewSet):
    queryset = Clinicians.objects.all()
    serializer_class = CliniciansSerializer


class CliniciansDatesViewSet(ModelViewSet):
    queryset = CliniciansDates.objects.all()
    serializer_class = CliniciansDatesSerializer


class CliniciansEducationViewSet(ModelViewSet):
    queryset = CliniciansEducation.objects.all()
    serializer_class = CliniciansEducationSerializer


class CliniciansExperienceViewSet(ModelViewSet):
    queryset = CliniciansExperience.objects.all()
    serializer_class = CliniciansExperienceSerializer


class CliniciansSpecialityViewSet(ModelViewSet):
    queryset = CliniciansSpeciality.objects.all()
    serializer_class = CliniciansSpecialitySerializer


class ConditionsViewSet(ModelViewSet):
    queryset = Conditions.objects.all()
    serializer_class = ConditionsSerializer


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CouponacceptViewSet(ModelViewSet):
    queryset = Couponaccept.objects.all()
    serializer_class = CouponacceptSerializer


class CouponsViewSet(ModelViewSet):
    queryset = Coupons.objects.all()
    serializer_class = CouponsSerializer


class DesignationViewSet(ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class DiscountcardViewSet(ModelViewSet):
    queryset = Discountcard.objects.all()
    serializer_class = DiscountcardSerializer


class DiscountcardFamilyViewSet(ModelViewSet):
    queryset = DiscountcardFamily.objects.all()
    serializer_class = DiscountcardFamilySerializer


class DiscountcardFamilyExtraViewSet(ModelViewSet):
    queryset = DiscountcardFamilyExtra.objects.all()
    serializer_class = DiscountcardFamilyExtraSerializer


class DistrictViewSet(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class FacilitiesViewSet(ModelViewSet):
    queryset = Facilities.objects.all()
    serializer_class = FacilitiesSerializer


class FacilitiesServicesViewSet(ModelViewSet):
    queryset = FacilitiesServices.objects.all()
    serializer_class = FacilitiesServicesSerializer


class FamilyViewSet(ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class HealthcheckbookingViewSet(ModelViewSet):
    queryset = Healthcheckbooking.objects.all()
    serializer_class = HealthcheckbookingSerializer


class HealthchecksViewSet(ModelViewSet):
    queryset = Healthchecks.objects.all()
    serializer_class = HealthchecksSerializer


class HealthchecksInclusionViewSet(ModelViewSet):
    queryset = HealthchecksInclusion.objects.all()
    serializer_class = HealthchecksInclusionSerializer


class HealthprovidersViewSet(ModelViewSet):
    queryset = Healthproviders.objects.all()
    serializer_class = HealthprovidersSerializer


class HealthprovidersSpecialityViewSet(ModelViewSet):
    queryset = HealthprovidersSpeciality.objects.all()
    serializer_class = HealthprovidersSpecialitySerializer


class HealthrecordsViewSet(ModelViewSet):
    queryset = Healthrecords.objects.all()
    serializer_class = HealthrecordsSerializer


class HealthseekerViewSet(ModelViewSet):
    queryset = Healthseeker.objects.all()
    serializer_class = HealthseekerSerializer


class HealthseekerAlertsViewSet(ModelViewSet):
    queryset = HealthseekerAlerts.objects.all()
    serializer_class = HealthseekerAlertsSerializer


class HealthseekerAvailabilitiesViewSet(ModelViewSet):
    queryset = HealthseekerAvailabilities.objects.all()
    serializer_class = HealthseekerAvailabilitiesSerializer


class HealthseekerHealthrecordsViewSet(ModelViewSet):
    queryset = HealthseekerHealthrecords.objects.all()
    serializer_class = HealthseekerHealthrecordsSerializer


class HealthseekerTypeViewSet(ModelViewSet):
    queryset = HealthseekerType.objects.all()
    serializer_class = HealthseekerTypeSerializer


class InterestViewSet(ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


class LanguagesViewSet(ModelViewSet):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer


class PhotoalbumViewSet(ModelViewSet):
    queryset = Photoalbum.objects.all()
    serializer_class = PhotoalbumSerializer


class PlansViewSet(ModelViewSet):
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer


class PlansGroupsViewSet(ModelViewSet):
    queryset = PlansGroups.objects.all()
    serializer_class = PlansGroupsSerializer


class PlansGroupsSpecialitiesViewSet(ModelViewSet):
    queryset = PlansGroupsSpecialities.objects.all()
    serializer_class = PlansGroupsSpecialitiesSerializer


class PriyorityViewSet(ModelViewSet):
    queryset = Priyority.objects.all()
    serializer_class = PriyoritySerializer


class ProfessionViewSet(ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class QualificationViewSet(ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class ReferrelsViewSet(ModelViewSet):
    queryset = Referrels.objects.all()
    serializer_class = ReferrelsSerializer


class ReferrelschemeViewSet(ModelViewSet):
    queryset = Referrelscheme.objects.all()
    serializer_class = ReferrelschemeSerializer


class RegistrationWelcomeMessageViewSet(ModelViewSet):
    queryset = RegistrationWelcomeMessage.objects.all()
    serializer_class = RegistrationWelcomeMessageSerializer


class ResellerpackagesViewSet(ModelViewSet):
    queryset = Resellerpackages.objects.all()
    serializer_class = ResellerpackagesSerializer


class ResellersViewSet(ModelViewSet):
    queryset = Resellers.objects.all()
    serializer_class = ResellersSerializer


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class SalesagentpackagesViewSet(ModelViewSet):
    queryset = Salesagentpackages.objects.all()
    serializer_class = SalesagentpackagesSerializer


class SalesagentsViewSet(ModelViewSet):
    queryset = Salesagents.objects.all()
    serializer_class = SalesagentsSerializer


class SalestargetViewSet(ModelViewSet):
    queryset = Salestarget.objects.all()
    serializer_class = SalestargetSerializer


class SecretquestionsViewSet(ModelViewSet):
    queryset = Secretquestions.objects.all()
    serializer_class = SecretquestionsSerializer


class SpecialityViewSet(ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SpecialityTypeViewSet(ModelViewSet):
    queryset = SpecialityType.objects.all()
    serializer_class = SpecialityTypeSerializer


class SponsorsViewSet(ModelViewSet):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer


class SponsorsGroupViewSet(ModelViewSet):
    queryset = SponsorsGroup.objects.all()
    serializer_class = SponsorsGroupSerializer


class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class SymptomsViewSet(ModelViewSet):
    queryset = Symptoms.objects.all()
    serializer_class = SymptomsSerializer


class TelephoneViewSet(ModelViewSet):
    queryset = Telephone.objects.all()
    serializer_class = TelephoneSerializer


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestCategoryViewSet(ModelViewSet):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer


class TestSubcategoryViewSet(ModelViewSet):
    queryset = TestSubcategory.objects.all()
    serializer_class = TestSubcategorySerializer


class TestimonialsViewSet(ModelViewSet):
    queryset = Testimonials.objects.all()
    serializer_class = TestimonialsSerializer


class TimeslotsViewSet(ModelViewSet):
    queryset = Timeslots.objects.all()
    serializer_class = TimeslotsSerializer


class TrxnAppointmentbookingsViewSet(ModelViewSet):
    queryset = TrxnAppointmentbookings.objects.all()
    serializer_class = TrxnAppointmentbookingsSerializer


class TrxnCouponsViewSet(ModelViewSet):
    queryset = TrxnCoupons.objects.all()
    serializer_class = TrxnCouponsSerializer


class TrxnDiscountcardViewSet(ModelViewSet):
    queryset = TrxnDiscountcard.objects.all()
    serializer_class = TrxnDiscountcardSerializer


class TrxnHealthcheckbookingViewSet(ModelViewSet):
    queryset = TrxnHealthcheckbooking.objects.all()
    serializer_class = TrxnHealthcheckbookingSerializer


class TrxnPaymentsViewSet(ModelViewSet):
    queryset = TrxnPayments.objects.all()
    serializer_class = TrxnPaymentsSerializer


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class WeekViewSet(ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer


class WellnessplanViewSet(ModelViewSet):
    queryset = Wellnessplan.objects.all()
    serializer_class = WellnessplanSerializer


class WellnessplanProfessionViewSet(ModelViewSet):
    queryset = WellnessplanProfession.objects.all()
    serializer_class = WellnessplanProfessionSerializer


class WellnessplanSocialhistoryViewSet(ModelViewSet):
    queryset = WellnessplanSocialhistory.objects.all()
    serializer_class = WellnessplanSocialhistorySerializer
