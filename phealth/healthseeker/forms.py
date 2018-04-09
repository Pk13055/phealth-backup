from django import forms

from api.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile', 'password', 'gender','dob')

    widgets = {
        'password': forms.PasswordInput()
    }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


class FamilyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile',  'gender','dob')

    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


class SeekerForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ('family', 'profession', 'language', )

    def __init__(self, *args, **kwargs):
        super(SeekerForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

#-----------------------------Language

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ('language','profession')

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField






