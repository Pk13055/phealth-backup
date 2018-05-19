from django import forms
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from psycopg2.extras import NumericRange
from querystring_parser import parser
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.viewsets import ModelViewSet

from api.models import *
from api.serializers import *
from phealth.utils import perdelta

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
        Q(location__landmark__icontains=params['location']) |
        Q(location__full_name__icontains=params['location'])).all()

    class LocationSerializer(ModelSerializer):
        class Meta:
            model = Location
            depth = 1
            fields = '__all__'

    class AppointmentSerializer(ModelSerializer):
        class Meta:
            model = Appointment
            depth = 1
            fields = ('date', 'time', 'duration',
                'from_timestamp', 'to_timestamp',)

    class ClinicianSerializer(ModelSerializer):

        # timings = SerializerMethodField()
        pending_appointments = SerializerMethodField()
        confirmed_appointments = SerializerMethodField()

        class Meta:
            model = Clinician
            depth = 5
            fields = '__all__'


        def get_pending_appointments(self, c):
            ''' gets the pending appointments for the given clinician '''
            apts = Appointment.objects.filter(under=c).filter(status='pending').all()
            return AppointmentSerializer(apts, many=True).data

        def get_confirmed_appointments(self, c):
            ''' gets the confirmed appointments for the given clinician '''
            apts = Appointment.objects.filter(under=c).filter(status='confirmed').all()
            return AppointmentSerializer(apts, many=True).data

        # def get_timings(self, c):
        #     ''' get the required timings array format as specified '''
        #     days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        #     timings = []
        #     get_time = lambda x: datetime.datetime.strptime(x, '%H:%M').time()
        #     sessions = [('morning', get_time('11:00')), ('afternoon', get_time('16:00')),
        #         ('evening', get_time('21:00')), ('night', get_time('23:59')),]
        #     for idx, day in enumerate(days):
        #         cur_day = {}
        #         cur_day['day'] = day
        #         start_w, end_w = c.work_timings[idx]
        #         start_b, end_b = c.break_timings[idx]
        #         work_t = perdelta(start_w, end_w, datetime.timedelta(minutes=30))
        #         work_t = list(zip(*[iter(work_t), iter(work_t[1:])]))
        #         break_t = perdelta(start_b, end_b, datetime.timedelta(minutes=30))
        #         break_t = list(zip(*[iter(break_t), iter(break_t[1:])]))
        #         work_t = [_ for _ in work_t if not any([_[0] >= i[0] or _[1] <= i[1] for i in break_t])]
        #         for session, time in sessions:
        #             cur_day[session] = [_ for _ in work_t if _[1] <= time]
        #             work_t = [_ for _ in work_t if _ not in cur_day[session]]
        #         timings.append(cur_day)
        #     return timings

    raw_locs = LocationSerializer([_.location for _ in hospitals], many=True)
    locations = raw_locs.data

    response['hospitals'] = [{'name' : _.name, 'id' : _.pk, 'location_id' : _.location.pk } for _ in hospitals]
    response['locations'] = locations
    response['languages'] = [_[0] for _ in Clinician.language_choices]

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


def get_appointment(request, appointment_uid):
    '''
        get appointment based on uid supplied

    '''

    class AppointmentSerializer(ModelSerializer):
        under = SerializerMethodField()
        provider = SerializerMethodField()

        def get_under(self, a):
            return {
                'name' : a.under.user.name,
                'id' : a.under.pk,
            }

        def get_provider(self, a):
            return {
                'name' : a.provider.name,
                'id' : a.provider.pk,
            }

        class Meta:
            model = Appointment
            depth = 1
            fields = '__all__'

    app = Appointment.objects.filter(uid=appointment_uid).first()
    if app:
        status = True
        data = AppointmentSerializer(app).data
    else:
        status = False
        data = ["No appointment matching UID"]

    return JsonResponse({
        'status' : status,
        'data' : data
    })


@require_POST
@csrf_exempt
def attach_user(request):
    '''
        @description This route is responsible for attaching an
        appointment object to a given user
        @param POST seeker_id int
        @param POST appointment_id int
        @return status, appointment object
    '''
    seeker_id = request.POST['seeker_id']
    appointment_id = request.POST['appointment_id']
    apt = Appointment.objects.filter(id=appointment_id).first()

    class AppointmentSerializer(ModelSerializer):
        class Meta:
            model = Appointment
            depth = 1
            fields = '__all__'

    if apt:
        status = True
        user = Seeker.objects.filter(id=seeker_id).first()
        if user:
            user.appointments.add(apt)
            data = AppointmentSerializer(apt).data
        else:
            status = False
            data = ["Invalid user (404)"]
    else:
        status = False
        data = ["Invalid Appointment (404)"]

    return JsonResponse({
        'status' : status,
        'data' : data,
    })

@require_POST
@csrf_exempt
def healthchecks_list(request, healthcheck=None):
    '''
        @description returns a list of the matching healthchecks
        @param request -> POST request
        @param applicability -> general/specific
        @param age_group -> 20-40
        @param gender -> male/female/both
        @param pre_existing_conditions_id -> speciality object id
    '''

    status = False
   
    class HealthCheckupSerializer(ModelSerializer):

        hospitals = SerializerMethodField()
        def get_hospitals(self, checkup):
            class ProviderSerializer(ModelSerializer):
                class Meta:
                    model = Provider
                    depth = 3
                    fields = ('location', 'specialities',
                    'facilities', 'offerings', 'special_checks', 'id',
                    'name', 'type',)
            return ProviderSerializer(checkup.provider_set.all(), many=True).data

        class Meta:
            model = HealthCheckup
            depth = 4
            fields = '__all__'
    if healthcheck:
        try:
            cur_check = HealthCheckup.objects.get(Q(uid=healthcheck) | Q(id=healthcheck))
            status = True
            data = HealthCheckupSerializer(cur_check).data
        except ValidationError:
            status = False
            data = ["Invalid UID/id"]

        return JsonResponse({
                'status' : status,
                'data' : data
            })
    if request.POST['applicability'].title() == 'Specific':

        applicability = 1
    else:
        applicability = 0

    speciality_objects_ids = Speciality.objects.filter(pk=request.POST['pre_existing_conditions_id']).values_list('id')
    healthchecks = HealthCheckup.objects.filter(applicability__icontains=applicability).filter(
        gender__icontains=request.POST['gender'])


    age_low, age_high = tuple(map(int, request.POST['age_group'].split('-')))
    age_range = NumericRange(age_low, age_high)
    healthchecks = healthchecks.filter(age__contained_by=age_range)

    data = HealthCheckupSerializer(healthchecks, many=True).data
    status = True

    return JsonResponse({
        'status' : status,
        'data' : data
    })


@require_POST
@csrf_exempt
def location_providers(request):
    '''
    Filtering providers with location and with selected healthchekup
    @description returns a list of the matching providers
    @param request -> POST request
    location: name str
    location_type: city/state str <hidden> (for example, if the client
        chooses hyderabad, Telengana as the choice, location_type should be
        set to the smallest subset, ie, city -> Hyderabad. If he chooses only
        Telengana, then it should set location_type as state)
    @param healthcheck_id -> healthcheck object id

    '''
    status = False
    location = request.POST['location']
    location_type = request.POST['location_type']
    healthchecks_object = HealthCheckup.objects.filter(
        pk=request.POST['healthcheck_id']).values_list('id')
    
    class HealthCheckupSerializer(ModelSerializer):

        class Meta:
            model = HealthCheckup
            depth = 4
            fields = '__all__'
    hospitals = Provider.objects.filter(
            Q(location__landmark__icontains=params['location']) |
            Q(location__full_name__icontains=params['location'])).all()
    providers = hospitals.filter(healthchecks__id__in=[13])


    data = HealthCheckupSerializer(providers, many=True).data
    status = True

    return JsonResponse({
        'status' : status,
        'data' : data
    })


# default API viewset

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


class SymptomViewSet(ModelViewSet):
    queryset = Symptoms.objects.all()
    serializer_class = SymptomSerializer


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
