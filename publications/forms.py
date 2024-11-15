from django import forms
from .models import *

class CommentaireForm(forms.ModelForm):
	description = forms.CharField(
		required=True, 
		label=False,
		widget=forms.Textarea(
			attrs={
				'class':'form-control mb-3',
				'rows':'2',
				'placeholder': 'Tapez votre comment...'
			}
	))

	class Meta:
		model = Commentaire 
		fields = ['description']
