from django import forms

from api.models import User
from api.models import Seeker


class RegistrationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['full_name'].widget.attrs.update({'class':'form-control'})
        self.fields['gender'].widget.attrs.update({'class':'form-control'})
        self.fields['dob'].widget.attrs.update({'class':'form-control'})
        self.fields['mobile_number'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        # self.fields['profile_pic'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Seeker
        fields = ['full_name','dob','mobile_number','gender','email']


class UserForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = User
        fields = ['password']