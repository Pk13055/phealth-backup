from random import randint
import requests
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import *
# Create your views here.
from api.models import User
from api.models import Seeker
from phealth.utils import signin
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render, get_object_or_404
from phealth.utils import  match_role, redirect, signin
from django.contrib.auth.hashers import make_password,check_password


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
    return render(request, 'healthseeker/dashboard.html', {})

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
    return render(request, 'healthseeker/registration/form3.html', {'form': form})


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
def step4(request):
    me = User.objects.get(pk=request.session['pk'])

    sc = Address.objects.filter(user=me).first()
    print(sc)
    if request.method == 'POST':
        if sc:
            form = AddressForm(request.POST, instance=sc)
        else:
            form = AddressForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = me
            post.save()
            print(post.pk)
            return redirect('healthseeker:step5')

    if sc:
        form = AddressForm(instance=sc)
    else:
        form = AddressForm
    states = State.objects.all()
    cities = City.objects.all()
    return render(request, 'healthseeker/registration/form4.html', {'form': form,'states':states,'cities':cities,'sc':sc})



def step5(request):

    return render(request,'healthseeker/registration/form5.html',{

    })

#----------------------------------------------step6


@match_role("healthseeker")
def step6(request):
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
    return render(request, 'healthseeker/registration/form6.html', {'form': form, 'lang': lang})


#--------------------------------------------------------

def family(request):
    print(request.GET)
    return render(request,'healthseeker/family_details.html',{})


def accountmanager(requset):

    return render(requset,'healthseeker/account_manager.html',{

    })

@match_role("healthseeker")
def contact(requset):
    me = User.objects.get(pk=requset.session['pk'])
    if requset.method == 'POST':
        form = AddressForm(requset.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = me
            return redirect('healthseeker:other')
    else:
        form = AddressForm
    states = State.objects.all()
    cities = City.objects.all()
    return render(requset, 'healthseeker/contact_details.html', {'form': form, 'states': states, 'cities': cities})


def intrest(requset):
    return render(requset,'healthseeker/manage_intrests.html',{})




def booking(requset):
    return render(requset,'healthseeker/booked.html',{})

def favaroitedoctors(requset):
    return render(requset,'healthseeker/favorite_decors.html',{})

def complaints(requset):
    return render(requset,'healthseeker/comlaints.html',{})

def healthalerts(requset):
    return render(requset,'healthseeker/health_alerts.html',{})

def schedule(request):
    return render(request, 'healthseeker/scheduled.html', {})


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


def other(request):

    return render(request,'healthseeker/other_info.html',{

    })
def records(request):

    return render(request,'healthseeker/health_records.html',{

    })
def changepassword(request):

    return render(request,'healthseeker/change_pswd.html',{

    })


