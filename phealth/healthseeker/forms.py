from django import forms

from api.models import Location, Post, Seeker, User, Familymember


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile', 'password', 'gender', 'dob', 'profile_pic')

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
        fields = ('name', 'email', 'mobile',  'gender','dob','profile_pic' )

    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)
        self.fields['relation'] = forms.ModelChoiceField(
            queryset=Familymember.objects.all())
            
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



class AddressForm(forms.ModelForm):
    # MODIFY THIS LATER ***
    class Meta:
        model = Location
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


class FriendForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'mobile', )

    def __init__(self, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['placeholder'] = myField


