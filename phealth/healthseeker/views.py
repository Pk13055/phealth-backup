import json
from random import randint

import requests
<<<<<<< HEAD
from django.contrib.auth.hashers import check_password, make_password
=======
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
>>>>>>> dev
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from querystring_parser import parser
<<<<<<< HEAD
from rest_framework.serializers import ModelSerializer

# Create your views here.
from api.models import Location, Seeker, User
=======
from rest_framework.serializers import ModelSerializer, SerializerMethodField

# Create your views here.
from api.models import (Alert, Appointment, Clinician, DiscountCard, Feedback,
                        Languages, Location, Provider, Seeker, User)
>>>>>>> dev
from phealth.utils import match_role, redirect, signin

from .forms import *


def SignIn(request):
    if request.method == "GET":
        return render(request, 'common/signin.html.j2', context={
            "title": "Login",
            "route": "/healthseeker",
            "color": "green"
        })
    elif request.method == "POST":
        print(request.POST)
        if signin("healthseeker", request):
            return redirect('healthseeker:dashboard')
        return redirect('healthseeker:signin')


@match_role("healthseeker")
def dashboard(request):
    me = User.objects.get(pk=request.session['pk'])
    email = User.objects.get(pk=request.session['pk'])
    part = Seeker.objects.get(user=me)
    print(part)

    #part = Seeker.objects.values('appointments').count()
    appointment = Seeker.objects.filter(user=me).values('appointments').count()
    print(me,"appointment=",appointment)
    healthchecks = Seeker.objects.filter(user=me).values('healthchecks').count()
    print(me,"healthchecks=",healthchecks)
    ps = 40
    if Seeker.objects.filter(family=me).count() > 0:
        ps +=20
    #if Address.objects.filter(user=me).count() > 0:
        #ps +=20

    if Seeker.objects.filter(user=me).values('profession'):
        ps +=20


    return render(request, 'healthseeker/dashboard.html', {
                                    'user': me,
                                    'email':email,
                                    'appointment':appointment,
                                    'healthchecks':healthchecks,
                                    'ps':ps

    })


def otp(request):
    if request.method == "POST":
        if (int(request.POST['otp']) == int(request.session['otp'])):
            request.POST = request.session['userdata']
            uform = UserForm(request.POST)
            upost = uform.save(commit=False)
            upost.role = "healthseeker"
            upost.password = make_password(request.POST['password'])
            upost.save()
            me = User.objects.get(email=request.session['userdata']['email'])
            s = Seeker.objects.create(user=me)
            print(me)
            #upost.save()
            if signin("healthseeker", request):
                return redirect('healthseeker:step2')
        else:
            return render(request,'healthseeker/registration/otp.html',{ 'error': "Invalid Otp"})

    else:
        return render(request,'healthseeker/registration/otp.html',{})


def registration(request):
    if request.method == 'POST':
        uform = UserForm(request.POST,request.FILES)
        if uform.is_valid():

            #otp here
            mobile = request.POST['mobile']
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['username'] = request.POST['email']
            request.POST._mutable = mutable

            request.session['userdata'] = request.POST
            otp = randint(1, 99999)
            request.session['otp'] = otp
            base_url = "http://api.msg91.com/api/sendhttp.php"
            params = {
                'sender': "CLICKH",
                'route': 4,
                'country': 91,
                'mobiles': [mobile],
                'authkey': '182461AjomJGPHB5a0041cb',
                'message': "Verification OTP : %d" % otp
            }
            r = requests.get(base_url, params=params)


            return redirect('healthseeker:otp')
    else:
        uform = UserForm()
    return render(request, 'healthseeker/registration/form1.html', context={
        "uform": uform,
    })


def step2(request):
    if request.method == 'POST':
        request.session['discountcard_id'] = request.POST['discountcard_id']
        return redirect('healthseeker:step3')
    cards = DiscountCard.objects.all()
    me = User.objects.get(pk=request.session['pk'])
    #s= Seeker.objects.create(user=me)
    #print(s)
    return render(request,'healthseeker/registration/form2.html',{'cards':cards})


@match_role("healthseeker")
def step3(request):
   me = User.objects.get(pk=request.session['pk'])


   if not request.session.get('discountcard_id'):
       return  redirect('healthseeker:step4')


   if request.method == 'POST':
       form = FamilyForm(request.POST)
       relation_object = Familymember.objects.get(id=request.POST['relation'])
       if form.is_valid():
           post = form.save(commit=False)
           post.role = "healthseeker"
           post.save()
           member = User.objects.get(pk=post.pk)
           Seeker.objects.create(user=member,family=me, relation=relation_object)
           return redirect('healthseeker:step3')
   else:
       form = FamilyForm()
   records = User.objects.all()


   data = User.objects.all()
   # print('data', data)
   seeker = Seeker.objects.filter(user=me)
   family = Seeker.objects.filter(family = me)
   count = family.count() + seeker.count()

   print('family ', family)

   #psobjs = Affiliation.objects.filter(ipId=x)
   #queryset = Sessions.objects.filter(sessionId__in=family.first)

   discountcard = DiscountCard.objects.get(pk = request.session['discountcard_id'])
   return render(request, 'healthseeker/registration/form3.html', {'form': form,'family':family ,
        'discountcard':discountcard, 'seeker': seeker, 'count': count})


@match_role("healthseeker")
def family_edit(request, pk):
   post = get_object_or_404(User, pk=pk)

   if request.method == "POST":
       seeker = Seeker.objects.get(user=post)
       form =FamilyForm(request.POST, instance=post)
       if form.is_valid():
           post = form.save(commit=False)
           post.save()

           seeker.relation = Familymember.objects.get(id=request.POST['relation'])
           seeker.save()

           return redirect('healthseeker:step3')
   else:
       form = FamilyForm(instance=post)
   return render(request, 'healthseeker/registration/familymember_edit.html', {'form': form})


@match_role("healthseeker")
def family_delete(request, pk):
   seeker = Seeker.objects.filter(user_id=pk)
   email = seeker.first().user.email
   seeker.delete()
   User.objects.filter(email=email).delete()
   return redirect('healthseeker:step3')

@match_role("healthseeker")
def form_view(request):
   result = User.objects.all()
   return render(request, 'healthseeker/registration/form3.html', {'values': result})


@match_role("healthseeker")
def form_edit(request, pk):
   post = get_object_or_404(User, pk=pk)
   if request.method == "POST":
       form = UserForm(request.POST, instance=post)
       if form.is_valid():
           post = form.save(commit=False)
           post.save()
           return redirect('healthseeker:form3_view')
   else:
       form = UserForm()
   return render(request, 'healthseeker/registration/from3.html', {'form': form})


@match_role("healthseeker")
def form3_delete(request, pk):
   result = User.objects.get(pk=pk)
   result.delete()
   return redirect('healthseeker:form3_view')


# def form3_edit(request, pk):
#     post = get_object_or_404(User, pk=pk)
#     if request.method == "POST":
#         form = UserForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.save()
#             return redirect('healthseeker:form3')
#     else:
#         form = UserForm(instance=post)
#     return render(request, 'healthseeker/registration/form3.html', {'form': form})


# @match_role("admin")
# def User_delete(request, pk):
#     result = User.objects.get(pk=pk)
#     result.delete()
#     return redirect('healthseeker:form_view')

<<<<<<< HEAD

@csrf_exempt
@match_role("healthseeker")
def step4(request):
=======
@match_role("healthseeker")
def step4(request):
    ''' enter the location details '''
>>>>>>> dev
    me = User.objects.get(pk=request.session['pk'])
    p = Seeker.objects.filter(user=me).first()
    message = None

    if request.method == "POST":
        data = parser.parse(request.POST.urlencode())
        place = json.loads(data['location'])
        extra_info = ', '.join(data['extra']).strip(' ')
        print(extra_info, json.dumps(place, indent=4), sep="\n")
        try:
            location = Location.objects.filter(full_name__icontains=place['formatted_address']).first()
            if not location:
                location = Location(place=place)
                location.extra = extra_info
            location.save()
            p.location = location
            p.save()
            return redirect('healthseeker:step5')
        except Exception as e:
            message = "Invalid Location! Please re-renter! (%s)" % str(e)

    return render(request, 'healthseeker/registration/form4.html', {
        'title' : "Account - Location Settings",
        'seeker' : p,
        'message' : message,
        })



def step5(request):
    me = User.objects.get(pk=request.session['pk'])
    ps = 40
    if Seeker.objects.filter(family=me).count() > 0:
        ps += 20
    elif Seeker.objects.filter(family=me).count() > 0:
        ps -=20
    #if Address.objects.filter(user=me).count() > 0:
        #ps += 20
    elif Seeker.objects.filter(family=me).count() > 0:
        ps -=20
    if Seeker.objects.get(user=me).profession:
        ps += 20
    elif Seeker.objects.filter(family=me).count() > 0:
        ps -=20
<<<<<<< HEAD

    return render(request,'healthseeker/registration/form5.html',{'ps':ps})
=======
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            # otp here
            mobile = request.POST['mobile']
            name = request.POST['name']
            request.session['userdata'] = request.POST
            otp = randint(1, 99999)
            request.session['otp'] = otp
            base = request.META['HTTP_REFERER']
            print(base)
            base_url = "http://api.msg91.com/api/sendhttp.php"
            params = {
                'sender': "CLICKH",
                'route': 4,
                'country': 91,
                'mobiles': [mobile],
                'authkey': '182461AjomJGPHB5a0041cb',
                'message': "Invitation Messsage :" + base,
            }
            r = requests.get(base_url, params=params)
            form = FriendForm(request.POST)
            upost = form.save(commit=False)
            upost.role = "healthseeker"
            me = User.objects.get(pk=request.session['pk'])
            s = Seeker.objects.get(user=me)
            print(me)
            upost.save()
            return redirect('healthseeker:step5')
    else:
        uform = FriendForm()
    return render(request, 'healthseeker/registration/form5.html', context={
        "uform": uform,
    })
>>>>>>> dev


@match_role("healthseeker")
def step6(request):
    me = User.objects.get(pk=request.session['pk'])
    sc = Seeker.objects.filter(user=me).first()
    ps = 40
    if Seeker.objects.filter(family=me).count() > 0:
        ps += 20
    #if Address.objects.filter(user=me).count() > 0:
        #ps += 20
    if Seeker.objects.get(user=me).profession:
        ps += 20
    if request.method == 'POST':
        if sc:
            form = LanguageForm(request.POST, instance=sc)
            sc.language = form.data.get('language')
            sc.profession = form.data.get('profession')
            sc.save()
        else:
            form = LanguageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = me
            return redirect('healthseeker:dashboard')

    if sc:
        form = LanguageForm(instance=sc)
    else:
        form = LanguageForm()
    lang = Languages.objects.all()
    print(me)
    return render(request, 'healthseeker/registration/form6.html', {'form': form, 'lang': lang, 'ps':ps})


@match_role("healthseeker")
def family(request):
   me = User.objects.get(pk=request.session['pk'])

   if not request.session.get('discountcard_id'):
       return  redirect('healthseeker:family')


   if request.method == 'POST':
       form = FamilyForm(request.POST, request.FILES)
       if form.is_valid():
           post = form.save(commit=False)
           post.role = "healthseeker"
           post.save()
           member = User.objects.get(pk=post.pk)
           Seeker.objects.create(user=member,family=me)
           return redirect('healthseeker:family')
   else:
       form = FamilyForm()
   records = User.objects.all()
   seeker = Seeker.objects.filter(user=me)


   data = User.objects.all()
   # print('data', data)
   family = Seeker.objects.filter(family = me)
   print(family.first())
   #psobjs = Affiliation.objects.filter(ipId=x)
   #queryset = Sessions.objects.filter(sessionId__in=family.first)


   discountcard = DiscountCard.objects.get(pk = request.session['discountcard_id'])
   return render(request, 'healthseeker/family_details.html', {'form': form,'family':family ,'discountcard':discountcard, 'seeker':seeker})

<<<<<<< HEAD
=======

>>>>>>> dev
@match_role("healthseeker")
def accountmanager(request):

    return render(request,'healthseeker/account_manager.html',{

    })


@csrf_exempt
@match_role("healthseeker")
def contact(request):
    me = User.objects.get(pk=request.session['pk'])
    p = Seeker.objects.filter(user=me).first()
    location = p.location
    message = None

    if request.method == "POST":
        data = parser.parse(request.POST.urlencode())
        extra_info = data['extra']
        loc_json = json.loads(data['location'])
        print(json.dumps(loc_json,indent=4))
        location = Location.objects.filter(full_name__icontains=loc_json['formatted_address']).first()
        message = "Location same as before!"
        if location is None :
            try:
                location = Location(place=loc_json)
                location.extra = extra_info
                location.save()
                p.location = location
                message = "Location successfully added & updated!"
            except Exception as e:
                message = "Invalid location! Please re-enter! (%s)" % str(e)
        elif location != p.location:
            location.extra = extra_info
            location.save()
            p.location = location
            message = "Location successfully updated!"

    p.save()
    return render(request, 'healthseeker/contact_details.html', {
        'title' : "Account - Location Settings",
        'seeker' : p,
        'message' : message,
        'location' : p.location.full_name,
        'extra_info' : p.location.extra,
    })


@match_role("healthseeker")
def favourite_doctors(request):
    ''' most commonly booked doctors '''

    seeker = Seeker.objects.filter(user__pk=request.session['pk']).first()
    TOTAL_COUNT = 3
    clinician_pks = list(filter(lambda _: _ is not None,
     seeker.appointments.values_list('under', flat=True)))
    counts = {}
    [counts.update({_: clinician_pks.count(_)}) for _ in clinician_pks]

    class ClinicianSerializer(ModelSerializer):
        mobile = SerializerMethodField()
        name = SerializerMethodField()
        profile_pic = SerializerMethodField()
        hospital_name = SerializerMethodField()
        address = SerializerMethodField()

        def get_name(self, c):
            return c.user.name

        def get_mobile(self, c):
            return c.user.mobile

        def get_profile_pic(self, c):
            return c.user.profile_pic

        def get_hospital_name(self, c):
            try:
                return c.provider_set.first().name
            except:
                return "Independent"

        def get_address(self, c):
            location = c.provider_set.first().location
            return {
                'full_name' : location.name,
                'place_id' : location.place_id,
                'location' : {
                    'lat' : location.lat,
                    'lng' : location.long,
                }
            }
        class Meta:
            model = Clinician
            fields = ('language', 'first_fee', 'fee',
            'education', 'experience_training',
            'procedure_conditions', 'awards',
            'registrations', 'name', 'profile_pic', 'mobile',
            'discount_offerings','hospital_name','address',)

    # get top few clinicians visited
    clinician_pks = sorted(counts, key=counts.get, reverse=True)[:TOTAL_COUNT]
    clinicians = Clinician.objects.filter(pk__in=clinician_pks)
    clinicians = ClinicianSerializer(clinicians, many=True)
    print(clinicians)
    return render(request, 'healthseeker/favourite_docs.html.j2', {
        'title' : "Favourite Doctors",
        'clinicians' :  clinicians.data,
    })


@match_role("healthseeker")
def complaints(request):
    me=User.objects.get(pk=request.session['pk'])
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('healthseeker:complaints')
    else:
        form=PostForm()
        print(form)
    result = Seeker.objects.get(user=me)
    print(result)
    return render(request,'healthseeker/comlaints.html',{'form':form,'result':result})

@match_role("healthseeker")
def healthalerts(request):
<<<<<<< HEAD
    return render(request,'healthseeker/health_alerts.html',{})


# Appointment Routes

=======
    ''' modify and book health alerts '''

    seeker = Seeker.objects.filter(user__pk=request.session['pk']).first()

    class AlertForm(forms.ModelForm):
        class Meta:
            model = Alert
            fields = ('name', 'duration', 'method',)

    alert_form = AlertForm()

    if request.method == "POST":
        req_type = request.POST['req_type']
        if req_type == "DELETE":
            alert = Alert.objects.filter(uid=request.POST['uid']).first()
            print(alert)
            alert.delete()
            return JsonResponse({
                'status' : True,
                'data' : "Alert has been successfully removed!"
            })
        elif req_type == "ADD":
            alert_form = AlertForm(request.POST, request.FILES)
            if 'uid' in request.POST:
                print("Existing")
                base_alert = Alert.objects.filter(uid=request.POST['uid']).first()
                alert_form = AlertForm(request.POST, request.FILES, instance=base_alert)
            if alert_form.is_valid():
                alert = alert_form.save(commit=False)
                alert.contact = seeker
                alert.type = request.POST['type']
                alert.save()
                print(alert)
        elif req_type == "MODIFY":
            class AlertSerializer(ModelSerializer):
                class Meta:
                    model = Alert
                    depth = 1
                    fields = ('uid', 'name', 'method', 'type', 'duration',)
            alert = Alert.objects.get(uid=request.POST['uid'])
            return JsonResponse({
                'status' : True,
                'data' : AlertSerializer(alert).data
            })

    return render(request, 'healthseeker/health_alerts.html.j2', {
        'title' : "Healthalerts",
        'alerts' : Alert.objects.filter(contact=seeker),
        'alert_types' : [_[0] for _ in Alert.alert_choices],
        'alert_form' : alert_form,
    })


# Appointment Routes

>>>>>>> dev
@match_role("healthseeker")
def appointment_booked(request):
    '''appointment route for the upcoming appointments'''

    seeker = Seeker.objects.filter(user__email=request.session['email']).first()
    records = seeker.appointments.filter(status='pending').order_by('-from_timestamp')

    return render(request,'healthseeker/appointment/appointment.html.j2',{
        'title' : "Appointment - Booked",
        'type' : 'booked',
        'records' : records,
    })


@match_role("healthseeker")
def appointment_scheduled(request):
    '''scheduled appointments'''

    seeker = Seeker.objects.filter(user__email=request.session['email']).first()
    records = seeker.appointments.filter(Q(status='confirmed') | Q(status='rescheduled')).order_by('-from_timestamp')

    return render(request,'healthseeker/appointment/appointment.html.j2', {
        'title' : "Appointment - Scheduled",
        'type' : 'scheduled',
        'records' : records,
    })


@match_role("healthseeker")
def appointment_past(request):
    ''' complete history of past appointments'''

    seeker = Seeker.objects.filter(user__email=request.session['email']).first()

    if request.method == "POST":
        # add feedback if valid
        params = parser.parse(request.POST.urlencode())
        print(params)
        try:
            ratings = {}
            [ratings.update({_ : float(params['categories'][_])}) for _ in params['categories']]
            apt = Appointment.objects.get(uid=params['apt_id'])
            provider = Provider.objects.get(pk=params['hosp_id'])
            clinician = provider.clinicians.get(pk=params['clinician_id'])
            feedback = Feedback(user=seeker, provider=provider,
                 clinician=clinician, appointment=apt,
                 categories=ratings, message=params['message'])
            feedback.save()
        except Exception as e:
            print("Error in feedback | %s" % str(e))

    records = seeker.appointments.filter(Q(status='completed')
        | Q(status='cancelled')).order_by('-from_timestamp')

    return render(request, 'healthseeker/appointment/appointment.html.j2', {
        'title' : 'Appointment - History',
        'type' : 'past',
        'records' : records,
        'review_cats' : Feedback.cat_keys.keys
    })


@match_role("healthseeker")
def reference(request):
    me = User.objects.get(pk=request.session['pk'])
    ps = 40
    if Seeker.objects.filter(family=me).count() > 0:
        ps += 20
    elif Seeker.objects.filter(family=me).count() > 0:
        ps -= 20
    #if Address.objects.filter(user=me).count() > 0:

        #ps += 20
    if request.method == 'POST':
        uform = FriendForm(request.POST)
        if uform.is_valid():
            # otp here
            mobile = request.POST['mobile']
            name = request.POST['name']
            request.session['userdata'] = request.POST
            otp = randint(1, 99999)
            request.session['otp'] = otp
            base = request.META['HTTP_REFERER']
            print(base)
            base_url = "http://api.msg91.com/api/sendhttp.php"
            params = {
                'sender': "CLICKH",
                'route': 4,
                'country': 91,
                'mobiles': [mobile],
                'authkey': '182461AjomJGPHB5a0041cb',
                'message': "Invitation Messsage :" + base,
            }
            r = requests.get(base_url, params=params)
            uform = FriendForm(request.POST)
            upost = uform.save(commit=False)
            upost.role = "healthseeker"
            me = User.objects.get(pk=request.session['pk'])
            s = Seeker.objects.get(user=me)
            print(me)
            upost.save()
            return redirect('healthseeker:reference')
    else:
        uform = FriendForm()
    return render(request, 'healthseeker/refer_earn.html', context={
        "uform": uform,
    })


<<<<<<< HEAD
=======

>>>>>>> dev
@match_role("healthseeker")
def information(request):
    me = User.objects.get(pk=request.session['pk'])
    if request.method == "POST":
        form = FamilyForm(request.POST, instance=me)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('healthseeker:family')
    else:
        form = FamilyForm(instance=me)
    return render(request, 'healthseeker/personal_information.html', {'form': form})


@match_role("healthseeker")
def other(request):
    me = User.objects.get(pk=request.session['pk'])
    sc = Seeker.objects.filter(user=me).first()
    if request.method == 'POST':
        if sc:
            form = LanguageForm(request.POST, instance=sc)
            sc.language = form.data.get('language')
            sc.profession = form.data.get('profession')
            sc.save()
        else:
            form = LanguageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = me
            return redirect('healthseeker:dashboard')

    if sc:
        form = LanguageForm(instance=sc)
    else:
        form = LanguageForm()
    lang = Languages.objects.all()
    return render(request, 'healthseeker/other_info.html', {'form': form, 'lang': lang})

<<<<<<< HEAD

=======
>>>>>>> dev
@match_role("healthseeker")
def records(request):

    return render(request,'healthseeker/health_records.html',{

    })
<<<<<<< HEAD


@match_role("healthseeker")
def changepassword(request):
=======
>>>>>>> dev


@match_role("healthseeker")
def intrests(request):

    return render(request, 'healthseeker/manage_intrests.html', {
        'title' : "Healthseeker - Interests"
    })
<<<<<<< HEAD
=======

@match_role("healthseeker")
def change_password(request):
    ''' method to change the seeker password '''

    seeker = Seeker.objects.filter(user__pk=request.session['pk']).first()
    status = None

    if request.method == "POST":
        if check_password(request.POST['old_password'], seeker.user.password):
            status = True
            seeker.user.password = make_password(request.POST['new_password'])
            seeker.user.save()
            disable_session = request.POST.get('disable_session', False) # do something with this
            if disable_session:
                return redirect('common:signout')
        else:
            status = False

    return render(request, 'healthseeker/change_password.html.j2', {
        'title' : "Account - Change password",
        'status' : status,
    })
>>>>>>> dev
