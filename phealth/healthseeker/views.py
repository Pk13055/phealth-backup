import json
from random import randint

import requests
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from querystring_parser import parser
from rest_framework.serializers import ModelSerializer

# Create your views here.
from api.models import (Appointment, Clinician, Feedback, Location, Provider,
                        Seeker, User)
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
    if Address.objects.filter(user=me).count() > 0:
        ps +=20

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
            me = User.objects.get(pk=request.session['pk'])
            s = Seeker.objects.get(user=me)
            print(me)
            upost.save()
            if signin("healthseeker", request):
                return redirect('healthseeker:step2')
        else:
            return render(request,'healthseeker/registration/otp.html',{ 'error': "Invalid Otp"})

    else:
        return render(request,'healthseeker/registration/otp.html',{})


def registration(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
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
    s= Seeker.objects.create(user=me)
    print(s)
    return render(request,'healthseeker/registration/form2.html',{'cards':cards})


@match_role("healthseeker")
def step3(request):
   me = User.objects.get(pk=request.session['pk'])

   if not request.session.get('discountcard_id'):
       return  redirect('healthseeker:step4')


   if request.method == 'POST':
       form = FamilyForm(request.POST)
       if form.is_valid():
           post = form.save(commit=False)
           post.role = "healthseeker"
           post.save()
           member = User.objects.get(pk=post.pk)
           Seeker.objects.create(user=member,family=me)
           return redirect('healthseeker:step3')
   else:
       form = FamilyForm()
   records = User.objects.all()


   data = User.objects.all()
   # print('data', data)
   family = Seeker.objects.filter(family = me)
   print(family.first())

   #psobjs = Affiliation.objects.filter(ipId=x)
   #queryset = Sessions.objects.filter(sessionId__in=family.first)

   discountcard = DiscountCard.objects.get(pk = request.session['discountcard_id'])
   return render(request, 'healthseeker/registration/form3.html', {'form': form,'family':family ,'discountcard':discountcard})


@match_role("healthseeker")
def family_edit(request, pk):
   post = get_object_or_404(User, pk=pk)
   if request.method == "POST":
       form =FamilyForm(request.POST, instance=post)
       if form.is_valid():
           post = form.save(commit=False)
           post.save()
           return redirect('healthseeker:step3')
   else:
       form = FamilyForm(instance=post)
   return render(request, 'healthseeker/registration/familymember_edit.html', {'form': form})


@match_role("healthseeker")
def family_delete(request, pk):
   result = User.objects.get(pk=pk)
   result.delete()
   return redirect('site_admin:step3')


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


@csrf_exempt
@match_role("healthseeker")
def step4(request):
    me = User.objects.get(pk=request.session['pk'])
    p = Seeker.objects.filter(user=me).first()
    print(p)
    if request.method == "POST":
        data = parser.parse(request.POST.urlencode())
        place = data['place']
        place['address_components'] = list(place['address_components'].values())
        for comp in place['address_components']:
            comp['types'] = comp['types']['']
            if isinstance(comp['types'], str):
                comp['types'] = [comp['types']]
        try:
            l = Location(place=place)
            l.save()
            status = True
            data = place
        except Exception as e:
            print(e)
            temp_loc = Location.objects.filter(full_name__icontains=place['formatted_address']).first()
            l = temp_loc or p.location
            if l == p.location:
                status = True
                data = ["Same Location as before!"]
            elif temp_loc is None:
                status = False
                data = [str(e)]
            else:
                status = True
                data = l

        p.location = l
        p.save()

        if isinstance(data, Location):
            class LocationSerializer(ModelSerializer):
                class Meta:
                    depth = 1
                    fields = ('lat', 'long', 'full_name', 'name',)
                    model = Location
            data = LocationSerializer(data).data

        return JsonResponse({
            'status' : status,
            'data' : data,
        })

    return render(request, 'healthseeker/registration/form4.html', {
        'title' : "Account - Location Settings",
        'seeker' : p,

    })


def step5(request):
    me = User.objects.get(pk=request.session['pk'])
    ps = 40
    if Seeker.objects.filter(family=me).count() > 0:
        ps += 20
    elif Seeker.objects.filter(family=me).count() > 0:
        ps -=20
    if Address.objects.filter(user=me).count() > 0:
        ps += 20
    elif Seeker.objects.filter(family=me).count() > 0:
        ps -=20
    if Seeker.objects.get(user=me).profession:
        ps += 20
    elif Seeker.objects.filter(family=me).count() > 0:
        ps -=20

    return render(request,'healthseeker/registration/form5.html',{'ps':ps})


@match_role("healthseeker")
def step6(request):
    me = User.objects.get(pk=request.session['pk'])
    sc = Seeker.objects.filter(user=me).first()
    ps = 40
    if Seeker.objects.filter(family=me).count() > 0:
        ps += 20
    if Address.objects.filter(user=me).count() > 0:
        ps += 20
    if Seeker.objects.get(user=me).profession:
        ps += 20
    if request.method == 'POST':
        if sc:
            form = LanguageForm(request.POST, instance=sc)
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
       form = FamilyForm(request.POST)
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


   data = User.objects.all()
   # print('data', data)
   family = Seeker.objects.filter(family = me)
   print(family.first())
   #psobjs = Affiliation.objects.filter(ipId=x)
   #queryset = Sessions.objects.filter(sessionId__in=family.first)


   discountcard = DiscountCard.objects.get(pk = request.session['discountcard_id'])
   return render(request, 'healthseeker/family_details.html', {'form': form,'family':family ,'discountcard':discountcard})


@match_role("healthseeker")
def accountmanager(request):

    return render(request,'healthseeker/account_manager.html',{

    })


@csrf_exempt
@match_role("healthseeker")
def contact(request):
    me = User.objects.get(pk=request.session['pk'])
    p = Seeker.objects.filter(user=me).first()
    print(p)

    if request.method == "POST":
        data = parser.parse(request.POST.urlencode())
        place = data['place']
        place['address_components'] = list(place['address_components'].values())
        for comp in place['address_components']:
            comp['types'] = comp['types']['']
            if isinstance(comp['types'], str):
                comp['types'] = [comp['types']]
        try:
            l = Location(place=place)
            l.save()
            status = True
            data = place
        except Exception as e:
            print(e)
            temp_loc = Location.objects.filter(full_name__icontains=place['formatted_address']).first()
            l = temp_loc or p.location
            if l == p.location:
                status = True
                data = ["Same Location as before!"]
            elif temp_loc is None:
                status = False
                data = [str(e)]
            else:
                status = True
                data = l

        p.location = l
        p.save()

        if isinstance(data, Location):
            class LocationSerializer(ModelSerializer):
                class Meta:
                    depth = 1
                    fields = ('lat', 'long', 'full_name', 'name',)
                    model = Location
            data = LocationSerializer(data).data
        return JsonResponse({
            'status' : status,
            'data' : data,
        })
    me = User.objects.get(pk=request.session['pk'])
    sobj = Seeker.objects.get(user=me)
    result = sobj.location
    data = result.full_name
    print(data)
    return render(request, 'healthseeker/contact_details.html', {
        'title' : "Account - Location Settings",
        'seeker' : p,
        'result':result,
        'data':data
        })


@match_role("healthseeker")
def interests(request):
    return render(request,'healthseeker/manage_intrests.html',{})


@match_role("healthseeker")
def favourite_doctors(request):
    return render(request,'healthseeker/favorite_decors.html',{})


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
    result = Seeker.objects.get(user=me)
    print(result)
    return render(request,'healthseeker/comlaints.html',{'form':form,'result':result})

@match_role("healthseeker")
def healthalerts(request):
    return render(request,'healthseeker/health_alerts.html',{})


# Appointment Routes

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

    return render(request,'healthseeker/refer_earn.html',{

    })


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


@match_role("healthseeker")
def records(request):

    return render(request,'healthseeker/health_records.html',{

    })


@match_role("healthseeker")
def changepassword(request):

    return render(request,'healthseeker/change_pswd.html',{

    })
