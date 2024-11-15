from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserInscriptionForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class UserModificationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']

class ProfilForm(forms.ModelForm):
	class Meta:
		model = Profil
		fields = ['nom_complet', 'description', 'image']


