from django import forms
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.context_processors import csrf
from django.db.models import Q
from django.views.decorators.http import require_POST
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.renderers import JSONRenderer
from querystring_parser import parser

from api.serializers import *
from api.models import *

# custom API views


@require_POST
@csrf_exempt
def doctors_list(request):
    ''' returns list of matching clinicians
    '''
    # symptomps location from to session
    params = parser.parse(request.POST.urlencode())
    required_params = ['from_date', 'to_date', 'session', 'symptom', 'location' , 'location_type']
    if len([True for _ in required_params if _ in params]) != len(required_params):
        return JsonResponse({
            'status' : False,
            'data' : {
                'error' : "Incomplete parameters"
            }})

    response = {}

    hospitals = Provider.objects.filter(
        Q(address__city__name__icontains=params['location']) |
        Q(address__city__state__name__icontains=params['location'])).all()

    class AddressSerializer(ModelSerializer):
            class Meta:
                model = Address
                depth = 5
                fields = '__all__'

    class ClinicianSerializer(ModelSerializer):
            class Meta:
                model = Clinician
                depth = 5
                fields = '__all__'

    raw_locs = AddressSerializer([_.address for _ in hospitals], many=True)
    locations = raw_locs.data

    response['hospitals'] = [_.name for _ in hospitals]
    response['locations'] = locations

    clinicians = {}
    for _ in hospitals:
        cur_clincians = _.clinicians.filter(specialities__name__icontains=params['symptom'])
        cur_clincians = [_ for _ in cur_clincians if
            _.check_session(params['session']) and
            _.check_availability(params['from_date'], params['to_date'])]
        raw_data = ClinicianSerializer(cur_clincians, many=True)
        clinicians[_.name] = raw_data.data

    response['clinicians'] = clinicians

    return JsonResponse({
        'status' : True,
        'data' : response
        })


@require_POST
@csrf_exempt
def make_appointment(request):

    class AppointmentForm(forms.ModelForm):
        class Meta:
            model = Appointment
            fields = ('date', 'time',)

    class AppointmentSerializer(ModelSerializer):
        class Meta:
            model = Appointment
            depth = 1
            fields = '__all__'

    form = AppointmentForm(request.POST, request.FILES)
    if form.is_valid():
        ap = form.save(commit=False)
        ap.provider = Provider.objects.filter(id=request.POST['provider_id']).first()
        ap.under = ap.provider.clinicians.filter(id=request.POST['clinician_id']).first()
        try:
            ap.save()
            data = AppointmentSerializer(ap).data
            status = True
        except:
            status = False
            data = ["Internal Error"]
    else:
        status = False
        data = form.errors

    return JsonResponse({
        'status' : status,
        'data' : data
        })


# default API viewset

class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


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


class CDNViewSet(ModelViewSet):
    queryset = CDN.objects.all()
    serializer_class = CDNSerializer


class BlogCategoryViewSet(ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class BlogCommentViewSet(ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
