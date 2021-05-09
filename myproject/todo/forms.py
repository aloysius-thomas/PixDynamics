from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from todo.models import Todomodel, UserRegistration


class TodoRegistrationForm(ModelForm):
    class Meta:
        model = Todomodel
        fields = '__all__'


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserRegistration
        fields = ("username", 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
