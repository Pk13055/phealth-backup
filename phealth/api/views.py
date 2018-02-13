from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from api.models import *


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class DistrictViewSet(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class TestCategoryViewSet(ModelViewSet):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer


class TestSubcategoryViewSet(ModelViewSet):
    queryset = TestSubcategory.objects.all()
    serializer_class = TestSubcategorySerializer


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class HealthCheckupViewSet(ModelViewSet):
    queryset = HealthCheckup.objects.all()
    serializer_class = HealthCheckupSerializer


class DiscountCardViewSet(ModelViewSet):
    queryset = DiscountCard.objects.all()
    serializer_class = DiscountCardSerializer


class SpecialityViewSet(ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class SeekerViewSet(ModelViewSet):
    queryset = Seeker.objects.all()
    serializer_class = SeekerSerializer


class ClinicianViewSet(ModelViewSet):
    queryset = Clinician.objects.all()
    serializer_class = ClinicianSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class ResellerViewSet(ModelViewSet):
    queryset = Reseller.objects.all()
    serializer_class = ResellerSerializer


class SalesAgentViewSet(ModelViewSet):
    queryset = SalesAgent.objects.all()
    serializer_class = SalesAgentSerializer


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class TestimonialViewSet(ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
