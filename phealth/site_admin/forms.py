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


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('name', 'code', 'department', 'description', 'subcategory')


    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)

class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ('name','quantity','validity','expiry','amount','type',)


    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField



class DiscountForm(forms.ModelForm):

    class Meta:
        model = DiscountCard
        fields = ('code', 'name', 'description', 'quantity', 'price', 'validity', 'health_checkups')


    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)

class SpecialityForm(forms.ModelForm):

    class Meta:
        model = Speciality
        fields = ('name', 'description',)


    def __init__(self, *args, **kwargs):
        super(SpecialityForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField
class TestcategoryForm(forms.ModelForm):

    class Meta:
        model = TestCategory
        fields = ('name', 'description',)


    def __init__(self, *args, **kwargs):
        super(TestcategoryForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


class HealthCheckupForm(forms.ModelForm):
    class Meta:
        model = HealthCheckup
        fields = ('name', 'description', 'price', 'image', 'tests')

    def __init__(self, *args, **kwargs):
        super(HealthCheckupForm, self).__init__(*args, **kwargs)

class FacilityForm(forms.ModelForm):

    class Meta:
        model = Facility
        fields = ('facility_type','name',)


    def __init__(self, *args, **kwargs):
        super(FacilityForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField




class TestsubcategoryForm(forms.ModelForm):

    class Meta:
        model = TestSubcategory
        fields = ('name', 'category','description',)


    def __init__(self, *args, **kwargs):
        super(TestsubcategoryForm, self).__init__(*args, **kwargs)
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

