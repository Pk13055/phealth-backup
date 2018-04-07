from django.shortcuts import render, redirect
from .forms import *
# Create your views here.
from api.models import User
from api.models import Seeker
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


def registration(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
        if uform.is_valid():
            upost = uform.save(commit=False)
            upost.role = "healthseeker"
            upost.password = make_password(request.POST['password'])
            upost.save()
            return redirect('healthseeker:form2')
    else:
        uform = UserForm()
    return render(request, 'healthseeker/registration/form1.html', context={
        "uform": uform,
    })


'''
def registration(request):

    if request.method == "POST":
        print(request.POST)
        form = RegistrationForm(request.POST)
        user = UserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            f = form.save(commit=False)
            email = request.POST['email']
            name = request.POST['full_name']
            mobile = request.POST['mobile_number']
            gender = request.POST['gender']
            password = make_password(request.POST['password'])
            u = User.objects.create(status=True,role="healthseeker",
                                     email=email,password=password,name=name,mobile=mobile,question_id=1)
            f.user = u
            f.save()
            # f.cleaned_data['']
            return redirect('healthseeker:form2')
    else:
        form = RegistrationForm()
        return render(request,'healthseeker/registration/form1.html',{'form':form})
'''
def registrationform2(request):
    return render(request,'healthseeker/registration/form2.html',{

    })


def registrationform3(request):

    return render(request,'healthseeker/registration/form3.html',{

    })

def addfamilymembers(request):
    print(request.GET)


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
