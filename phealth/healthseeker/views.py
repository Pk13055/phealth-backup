from random import randint
import requests
import json
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import *
# Create your views here.
from api.models import User,Location
from api.models import Seeker
from phealth.utils import signin
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render, get_object_or_404
from phealth.utils import  match_role, redirect, signin
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from querystring_parser import parser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.serializers import ModelSerializer
from django.http import HttpResponse, JsonResponse


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



def dashboard(request):
    me = User.objects.get(pk=request.session.get("pk"))
    email = User.objects.get(pk=request.session.get("pk"))
    part = Seeker.objects.get(user=me)
    #part = Seeker.objects.values('appointments').count()
    appointment = part.appointments.all().count()

    healthchecks = HealthCheckup.objects.count()
    ps = 40
    if Seeker.objects.filter(family=me).count() > 0:
        ps +=20
    if Address.objects.filter(user=me).count() > 0:
        ps +=20

    if Seeker.objects.get(user=me).profession:
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
    return render(request,'healthseeker/registration/form2.html',{'cards':cards})

#-----------------------------------------------------------------------------------------------
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




'''
def form3_edit(request, pk):
    post = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('healthseeker:form3')
    else:
        form = UserForm(instance=post)
    return render(request, 'healthseeker/registration/form3.html', {'form': form})



@match_role("admin")
def User_delete(request, pk):
    result = User.objects.get(pk=pk)
    result.delete()
    return redirect('healthseeker:form_view')'''




#------------------------------------------------------------------------------
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
    me = User.objects.get(pk=request.session.get("pk"))
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

#----------------------------------------------step6


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
            post.save()
            return redirect('healthseeker:dashboard')

    if sc:
        form = LanguageForm(instance=sc)
    else:
        form = LanguageForm()
    lang = Languages.objects.all()
    print(me)
    return render(request, 'healthseeker/registration/form6.html', {'form': form, 'lang': lang, 'ps':ps})


#--------------------------------------------------------

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


#---------------------------------------------------------------------------------

def accountmanager(requset):

    return render(requset,'healthseeker/account_manager.html',{

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

    return render(request, 'healthseeker/contact_details.html', {
        'title' : "Account - Location Settings",
        'seeker' : p,

    })


def intrest(requset):
    return render(requset,'healthseeker/manage_intrests.html',{})


#-----------------------------------------------------------------------------------------------------------
@match_role("healthseeker")
def booking(request):
    me = User.objects.get(pk=request.session['pk'])
    sobj = Seeker.objects.get(user=me)
    result = sobj.appointments.all()
    return render(request, 'healthseeker/booked.html', {'values': result})
#-----------------------------------------------------------------------------------------------------------

def favaroitedoctors(requset):
    return render(requset,'healthseeker/favorite_decors.html',{})

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

def healthalerts(requset):
    return render(requset,'healthseeker/health_alerts.html',{})

def schedule(request):
    me = User.objects.get(pk=request.session['pk'])
    sobj = Seeker.objects.get(user=me)
    result = sobj.appointments.all()
    return render(request, 'healthseeker/scheduled.html', {'values': result})


def reference(request):

    return render(request,'healthseeker/refer_earn.html',{

    })

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
#---------------------------------------------------------------------------------------

match_role("healthseeker")
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
            post.save()
            return redirect('healthseeker:dashboard')

    if sc:
        form = LanguageForm(instance=sc)
    else:
        form = LanguageForm()
    lang = Languages.objects.all()
    return render(request, 'healthseeker/other_info.html', {'form': form, 'lang': lang})

def records(request):

    return render(request,'healthseeker/health_records.html',{

    })
def changepassword(request):

    return render(request,'healthseeker/change_pswd.html',{

    })

    