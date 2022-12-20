from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    l_username = forms.CharField(label='Username or Email', max_length=50, required=True, widget=forms.TextInput())
    l_password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())


class UserRegistrationForm(forms.ModelForm):
    r_password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())
    r_password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput())
    r_username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['r_password'] != cd['r_password2']:
            raise forms.ValidationError('Password are not the same')
        return cd['r_password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

    photo = forms.ImageField(label='', widget=forms.FileInput())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
