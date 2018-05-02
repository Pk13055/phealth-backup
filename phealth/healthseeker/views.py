from random import randint

import requests
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from api.models import Seeker, User
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
            return redirect('healthseeker:contactdetails')
        return redirect('healthseeker:signin')


def healthseekersignin(request):
    if request.method == "POST":
        data = request.POST
        if signin("admin", data):
            return redirect('healthseeker:healthseekerdashboard_home')
    return render(request,'healthseeker/sigin.html',{})

def healthseekerdashboard(request):
    pass

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
                return redirect('healthseeker:step3')
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



def registrationform2(request):
    return render(request,'healthseeker/registration/form2.html',{

    })

#-----------------------------------------------------------------------------------------------


@match_role("healthseeker")
def step3(request):
    #me = User.objects.get(pk=)
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.role = "healthseeker"
            post.save()
            member = User.objects.get(pk=post.pk)
            me = User.objects.get(pk=request.session['pk'])
            Seeker.objects.create(user=member,family=me)
            return redirect('healthseeker:step3')
    else:
        form = FamilyForm()
    u = User.objects.all()
    return render(request, 'healthseeker/registration/form3.html', {'form': form,'users':u })


@match_role("healthseeker")
def family_edit(request, pk):
    post = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form =FamilyForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_admin:step3')
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
        form = User(instance=post)
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
def registrationform4(request):

    return render(request, 'healthseeker/registration/form4.html', {

    })

def registrationform5(request):

    return render(request,'healthseeker/registration/form5.html',{

    })

def addfamilymembers(request):
    print(request.GET)
    return render(request,'healthseeker/family_details.html',{})


def accountmanager(requset):

    return render(requset,'healthseeker/account_manager.html',{

    })

@match_role("healthseeker")
def contactdetails(requset):

    return render(requset,'healthseeker/contact_details.html',{

    })

def intrest(requset):
    return render(requset,'healthseeker/manage_intrests.html',{})





def favaroitedoctors(requset):
    return render(requset,'healthseeker/favorite_decors.html',{})

def complaints(requset):
    return render(requset,'healthseeker/comlaints.html',{})

def healthalerts(requset):
    return render(requset,'healthseeker/health_alerts.html',{})

# Appointment Routes


def appointment_booked(request):
    '''appointment route for the upcoming appointments'''

    seeker = Seeker.objects.filter(user__email=request.session['email']).first()
    records = seeker.appointments.filter(status='pending').order_by('-from_timestamp')

    return render(request,'healthseeker/appointment/appointment.html.j2',{
        'title' : "Appointment - Booked",
        'type' : 'booked',
        'records' : records,
    })


def appointment_scheduled(request):
    '''scheduled appointments'''

    seeker = Seeker.objects.filter(user__email=request.session['email']).first()
    records = seeker.appointments.filter(Q(status='confirmed') | Q(status='rescheduled')).order_by('-from_timestamp')

    return render(request,'healthseeker/appointment/appointment.html.j2', {
        'title' : "Appointment - Scheduled",
        'type' : 'scheduled',
        'records' : records,
    })


def appointment_past(request):
    ''' complete history of past appointments'''

    seeker = Seeker.objects.filter(user__email=request.session['email']).first()
    records = seeker.appointments.filter(Q(status='completed') | Q(status='cancelled')).order_by('-from_timestamp')

    return render(request, 'healthseeker/appointment/appointment.html.j2', {
        'title' : 'Appointment - History',
        'type' : 'past',
        'records' : records,
    })


def reference(request):

    return render(request,'healthseeker/refer_earn.html',{

    })

def personalinformation(request):

    return render(request,'healthseeker/personal_information.html',{

    })

def otherinformation(request):

    return render(request,'healthseeker/other_info.html',{

    })
def records(request):

    return render(request,'healthseeker/health_records.html',{

    })
def changepassword(request):

    return render(request,'healthseeker/change_pswd.html',{

    })
