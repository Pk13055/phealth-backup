from django import forms

from api.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile', 'password', 'gender',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


class SeekerForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ('family', 'profession', 'language', 'dob',)

    def __init__(self, *args, **kwargs):
        super(SeekerForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

class DobForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ( 'dob',)

    def __init__(self, *args, **kwargs):
        super(DobForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField




