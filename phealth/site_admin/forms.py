from django import forms

from api.models import *

class SymptomsForm(forms.ModelForm):

    class Meta:
        model = Symptoms
        fields = ('name', 'symptomarea',)


    def __init__(self, *args, **kwargs):
        super(SymptomsForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ('name','quantity','validity','expiry','amount','type',)


    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

class FacilityForm(forms.ModelForm):

    class Meta:
        model = Facility
        fields = ('facility_type','name',)


    def __init__(self, *args, **kwargs):
        super(FacilityForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField



class FacilityTypeForm(forms.ModelForm):

    class Meta:
        model = FacilityType
        fields = ('service_type','name',)


    def __init__(self, *args, **kwargs):
        super(FacilityTypeForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField