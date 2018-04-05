from django.shortcuts import render, redirect

# Create your views here.
from api.models import User
from api.models import Seeker
from healthseeker.forms import RegistrationForm, UserForm
from phealth.utils import signin
from django.contrib.auth.hashers import make_password


def healthseekersignin(request):
    if request.method == "POST":
        data = request.POST
        if signin("admin", data):
            return redirect('healthseeker:healthseekerdashboard_home')
    return render(request,'healthseeker/sigin.html',{})

def healthseekerdashboard(request):
    pass



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

def registrationform2(request):
    return render(request,'healthseeker/registration/form2.html',{

    })


def registrationform3(request):

    return render(request,'healthseeker/registration/form3.html',{

    })

def addfamilymembers(request):
    print(request.GET)