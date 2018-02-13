from rest_framework.serializers import HyperlinkedModelSerializer
from api.models import *


class CountrySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Country
        depth = 6
        fields = '__all__'


class StateSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = State
        depth = 6
        fields = '__all__'


class CitySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = City
        depth = 6
        fields = '__all__'


class DistrictSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = District
        depth = 6
        fields = '__all__'


class AddressSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Address
        depth = 6
        fields = '__all__'


class CouponSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Coupon
        depth = 6
        fields = '__all__'


class TestCategorySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = TestCategory
        depth = 6
        fields = '__all__'


class TestSubcategorySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = TestSubcategory
        depth = 6
        fields = '__all__'


class TestSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Test
        depth = 6
        fields = '__all__'


class HealthCheckupSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = HealthCheckup
        depth = 6
        fields = '__all__'


class DiscountCardSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = DiscountCard
        depth = 6
        fields = '__all__'


class SpecialitySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Speciality
        depth = 6
        fields = '__all__'


class QuestionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Question
        depth = 6
        fields = '__all__'


class UserSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = User
        depth = 6
        fields = '__all__'


class TransactionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Transaction
        depth = 6
        fields = '__all__'


class SeekerSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Seeker
        depth = 6
        fields = '__all__'


class ClinicianSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Clinician
        depth = 6
        fields = '__all__'


class ProviderSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Provider
        depth = 6
        fields = '__all__'


class SponsorSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Sponsor
        depth = 6
        fields = '__all__'


class ResellerSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Reseller
        depth = 6
        fields = '__all__'


class SalesAgentSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = SalesAgent
        depth = 6
        fields = '__all__'


class AppointmentSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Appointment
        depth = 6
        fields = '__all__'


class TestimonialSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Testimonial
        depth = 6
        fields = '__all__'
