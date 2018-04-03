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

class TestsubcategoryForm(forms.ModelForm):

    class Meta:
        model = TestSubcategory
        fields = ('name', 'category','description',)


    def __init__(self, *args, **kwargs):
        super(TestsubcategoryForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField