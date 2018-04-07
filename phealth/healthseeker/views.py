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

#-----------------------------------------------------------------------------------------------


@match_role("healthseeker")
def form_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('healthseeker:form3_view')
    else:
        form = UserForm()
    return render(request, 'healthseeker/registration/form3.html', {'form': form})


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