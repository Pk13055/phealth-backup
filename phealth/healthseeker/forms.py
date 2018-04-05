from django import forms

from api.models import User
from api.models import Seeker


class RegistrationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['dob'].widget.attrs.update({'class':'form-control'})

        # self.fields['profile_pic'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Seeker
        fields = ['dob']


class UserForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = User
        fields = ['password']