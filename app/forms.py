

from django.forms import ModelForm
from .models import Notes, Label
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class NoteForm(ModelForm):
    class Meta:
        model = Notes
        fields = ('title', 'note',)