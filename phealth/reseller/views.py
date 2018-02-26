from django.shortcuts import render, redirect
from phealth.utils import signin, match_role
from api.models import Reseller, SalesAgent
# Create your views here.


def SignIn(request):
	'''
		signin route for the reseller

	'''
	if request.method == "GET":
		return render(request, 'common/signin.html.j2', context={
			"title": "Reseller Login",
			"route": "/reseller",
			"color": "danger"
		})
	elif request.method == "POST":
		if signin("reseller", request):
			return redirect('reseller:dashboard_home')
		return redirect('reseller:signin')


def SignUp(request):
	''' signup route for the reseller
	'''
	return redirect('reseller:dashboard_home')

# Main dashboard routes

@match_role("reseller")
def dashboard(request):
	''' main dashboard route
	'''
	r = Reseller.objects.filter(user__email = request.session['email']).first()
	u = r.user
	class UserForm(forms.ModelForm):

		class Meta:
			model = User
			fields = ('name', 'email', 'mobile', 'gender',
			 'question', 'answer', 'profile_pic')

	if request.method == 'POST':
		# c = ClinicianForm(request.POST, request.FILES, instance=u)
		b = UserForm(request.POST, request.FILES, instance=u)
		if b.is_valid():
			b.save()

	return render(request, 'reseller/dashboard/home.html.j2', context={
			'title' : "Basic Details",
			'form_title' : "Edit basic information",
			'user_form' : UserForm(instance = u)
		})

@match_role("reseller")
def view_discounts(request):
	''' route for discount card handling
	'''
	r = Reseller.objects.filter(user__email = request.session['email']).first()
	discounts = r.discount_cards

	return render(request, 'reseller/dashboard/discounts.html.j2', context={
			'title' : "Discount Cards",
		})
