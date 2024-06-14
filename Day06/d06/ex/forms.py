from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class Signin(forms.Form):
    username = forms.CharField(label='username', min_length=3, max_length=10)
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = None
        try:
            user = User.objects.get(username=cleaned_data.get("username"))
        except Exception as e:
            raise forms.ValidationError("Invalid username")
        if check_password(password, user.password) == False:
            raise forms.ValidationError("Invalid password")
        return cleaned_data

class Signup(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', max_length=32, widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            print("ca marche pas")
            raise forms.ValidationError("Passwords don't match")
        print("ca marche")
        return password2

    def clean_username(self):
       username = self.cleaned_data['username']
       if User.objects.filter(username=username).exists():
           raise forms.ValidationError('Username already exists.')
       return username

class For_tip(forms.Form):
    text = forms.CharField(label="Text", max_length=1000)
