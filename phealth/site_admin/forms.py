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
#------------------------------Symptoms area form

class SymptomsareaForm(forms.ModelForm):

    class Meta:
        model = SymptomsArea
        fields = ('speciality', 'name', 'created_date')


    def __init__(self, *args, **kwargs):
        super(SymptomsareaForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField






#----------------------------------------------------------------




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
        fields = (
        'code', 'name', 'image', 'description', 'quantity', 'coverage', 'restriction', 'applicable_family_members',
        'applicability', 'group_or_sponsor', 'price', 'price_extra_member', 'extra_family_members', 'validity',
        'health_checkups', 'coupon',)

    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField
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
        fields = ('name', 'description', 'price', 'image', 'tests', 'applicability', 'group_or_sponsor', 'coupon',)

    def __init__(self, *args, **kwargs):
        super(HealthCheckupForm, self).__init__(*args, **kwargs)
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


#appointments daily
class AppointmentsForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('date','time', 'duration', 'status','under', 'provider')


    def __init__(self, *args, **kwargs):
        super(AppointmentsForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

class TimesessionForm(forms.ModelForm):

    class Meta:
        model = Timesession
        fields = ('name', 'fromtime', 'totime',)

    def __init__(self, *args, **kwargs):
        super(TimesessionForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

#--------------------RoleForm------------------------------------------------
class RoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ('name', 'subrole')

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


#--------------------RoleForm------------------------------------------------


class HealthProviderPlansForm(forms.ModelForm):

    class Meta:
        model = HealthProviderPlans
        fields = ('name','price','amount_credit','image','description','first_consultation_share','subsequent_consultation_share','first_consultation_discount','subsequent_consultation_discount','validity','speciality_group','software_licence','applicability','service_provider','coupon')

    def __init__(self, *args, **kwargs):
        super(HealthProviderPlansForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField

#-------------------------------------ID Configurations-----------------------------------


class IdConfigurationForm(forms.ModelForm):

    class Meta:
        model = IdConfiguration
        fields = ('affix','prefix','tablename')

    def __init__(self, *args, **kwargs):
        super(IdConfigurationForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


