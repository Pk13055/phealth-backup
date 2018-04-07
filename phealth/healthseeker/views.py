from random import randint
import requests
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
                return redirect('healthseeker:contactdetails')
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
def registrationform3(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
        nform = DobForm(request.POST)
        if uform.is_valid() and nform.is_valid():
            upost = uform.save(commit=False)
            upost.save()
            npost = nform.save(commit=False)
            npost.save()
            return redirect('healthseeker:form2')
    else:
        uform = UserForm()
        nform = DobForm()
        result = User.objects.all()
    return render(request, 'healthseeker/registration/form3.html', context={
        "uform": uform,
        "nform": nform,
        "values": result,
    })

def registrationform3(request, pk):
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



def registrationform3(request, pk):
    result = User.objects.get(pk=pk)
    result.delete()
    return redirect('healthseeker:form3')


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




def booking(requset):
    return render(requset,'healthseeker/booked.html',{})

def favaroitedoctors(requset):
    return render(requset,'healthseeker/favorite_decors.html',{})

def complaints(requset):
    return render(requset,'healthseeker/comlaints.html',{})

def healthalerts(requset):
    return render(requset,'healthseeker/health_alerts.html',{})

def schedule(request):

    return render(request,'healthseeker/scheduled.html',{

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