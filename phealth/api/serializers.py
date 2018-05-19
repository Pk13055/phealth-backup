from rest_framework.serializers import HyperlinkedModelSerializer
from api.models import *
from rest_framework import serializers


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

class SymptomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Symptoms
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


class SpecialitySerializer(serializers.ModelSerializer):

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


class CDNSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = CDN
        depth = 6
        fields = '__all__'


class BlogCategorySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = BlogCategory
        depth = 6
        fields = '__all__'


class PostSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Post
        depth = 6
        fields = '__all__'


class BlogCommentSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = BlogComment
        depth = 6
        fields = '__all__'
