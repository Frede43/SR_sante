from django import forms
from .models import Question, Comment

# Form to create a new question
class QuestionForm(forms.ModelForm):
	content = forms.CharField(
		required=True, 
		label=False,
		widget=forms.Textarea(
			attrs={
				'class':'form-control mb-3',
				'rows':'4',
				'placeholder': 'Tapez votre question...'
			}
	))
	class Meta:
		model = Question
		fields = ['title', 'content']

# Form to create a comment or reply
class CommentForm(forms.ModelForm):
	content = forms.CharField(
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
		model = Comment
		fields = ['content']


