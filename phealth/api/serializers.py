from rest_framework import serializers
from api.models import *



class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class AgegroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Agegroup
        fields = '__all__'


class AlertsourcesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Alertsources
        fields = '__all__'


class AlerttypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Alerttype
        fields = '__all__'


class AppointmentbookingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Appointmentbooking
        fields = '__all__'


class AvailablefacilitiesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Availablefacilities
        fields = '__all__'


class BookingsourcesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bookingsources
        fields = '__all__'


class BusinessregtypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Businessregtype
        fields = '__all__'


class CitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class ClinicianMembershipsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ClinicianMemberships
        fields = '__all__'


class CliniciansSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Clinicians
        fields = '__all__'


class CliniciansDatesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CliniciansDates
        fields = '__all__'


class CliniciansEducationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CliniciansEducation
        fields = '__all__'


class CliniciansExperienceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CliniciansExperience
        fields = '__all__'


class CliniciansSpecialitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CliniciansSpeciality
        fields = '__all__'


class ConditionsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Conditions
        fields = '__all__'


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class CouponacceptSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Couponaccept
        fields = '__all__'


class CouponsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Coupons
        fields = '__all__'


class DesignationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Designation
        fields = '__all__'


class DiscountcardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Discountcard
        fields = '__all__'


class DiscountcardFamilySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DiscountcardFamily
        fields = '__all__'


class DiscountcardFamilyExtraSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DiscountcardFamilyExtra
        fields = '__all__'


class DistrictSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = District
        fields = '__all__'


class FacilitiesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Facilities
        fields = '__all__'


class FacilitiesServicesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FacilitiesServices
        fields = '__all__'


class FamilySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Family
        fields = '__all__'


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Feedback
        fields = '__all__'


class GenderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class HealthcheckbookingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Healthcheckbooking
        fields = '__all__'


class HealthchecksSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Healthchecks
        fields = '__all__'


class HealthchecksInclusionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HealthchecksInclusion
        fields = '__all__'


class HealthprovidersSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Healthproviders
        fields = '__all__'


class HealthprovidersSpecialitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HealthprovidersSpeciality
        fields = '__all__'


class HealthrecordsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Healthrecords
        fields = '__all__'


class HealthseekerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Healthseeker
        fields = '__all__'


class HealthseekerAlertsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HealthseekerAlerts
        fields = '__all__'


class HealthseekerAvailabilitiesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HealthseekerAvailabilities
        fields = '__all__'


class HealthseekerHealthrecordsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HealthseekerHealthrecords
        fields = '__all__'


class HealthseekerTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HealthseekerType
        fields = '__all__'


class InterestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Interest
        fields = '__all__'


class LanguagesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Languages
        fields = '__all__'


class PhotoalbumSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Photoalbum
        fields = '__all__'


class PlansSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Plans
        fields = '__all__'


class PlansGroupsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PlansGroups
        fields = '__all__'


class PlansGroupsSpecialitiesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PlansGroupsSpecialities
        fields = '__all__'


class PriyoritySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Priyority
        fields = '__all__'


class ProfessionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profession
        fields = '__all__'


class QualificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Qualification
        fields = '__all__'


class ReferrelsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Referrels
        fields = '__all__'


class ReferrelschemeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Referrelscheme
        fields = '__all__'


class RegistrationWelcomeMessageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RegistrationWelcomeMessage
        fields = '__all__'


class ResellerpackagesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resellerpackages
        fields = '__all__'


class ResellersSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resellers
        fields = '__all__'


class RoleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class SalesagentpackagesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Salesagentpackages
        fields = '__all__'


class SalesagentsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Salesagents
        fields = '__all__'


class SalestargetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Salestarget
        fields = '__all__'


class SecretquestionsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Secretquestions
        fields = '__all__'


class SpecialitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Speciality
        fields = '__all__'


class SpecialityTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SpecialityType
        fields = '__all__'


class SponsorsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sponsors
        fields = '__all__'


class SponsorsGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SponsorsGroup
        fields = '__all__'


class StateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = State
        fields = '__all__'


class SymptomsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Symptoms
        fields = '__all__'


class TelephoneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Telephone
        fields = '__all__'


class TestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Test
        fields = '__all__'


class TestCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TestCategory
        fields = '__all__'


class TestSubcategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TestSubcategory
        fields = '__all__'


class TestimonialsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Testimonials
        fields = '__all__'


class TimeslotsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Timeslots
        fields = '__all__'


class TrxnAppointmentbookingsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrxnAppointmentbookings
        fields = '__all__'


class TrxnCouponsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrxnCoupons
        fields = '__all__'


class TrxnDiscountcardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrxnDiscountcard
        fields = '__all__'


class TrxnHealthcheckbookingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrxnHealthcheckbooking
        fields = '__all__'


class TrxnPaymentsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrxnPayments
        fields = '__all__'


class UsersSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class WeekSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Week
        fields = '__all__'


class WellnessplanSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Wellnessplan
        fields = '__all__'


class WellnessplanProfessionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WellnessplanProfession
        fields = '__all__'


class WellnessplanSocialhistorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WellnessplanSocialhistory
        fields = '__all__'
