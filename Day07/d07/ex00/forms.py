from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import Textarea, HiddenInput
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",  "password1", "password2")

class PublishForm(forms.Form):
    title = forms.CharField(max_length=64, required=True)
    synopsis = forms.CharField(max_length=312, required=True)
    content = forms.CharField(widget=Textarea(), required=True)

class FavouriteForm(forms.Form):
    article = forms.IntegerField(widget=HiddenInput(), required=True)

    def __init__(self, article, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if article is not None:
            self.fields['article'].initial = article

class LoginForm(forms.Form):
    name = forms.CharField(label='Name', max_length=32)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)