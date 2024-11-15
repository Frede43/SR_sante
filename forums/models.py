from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
# Question model for forum posts
class Question(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('question_detail', args=[self.pk])


# Comment model for comments on questions or other comments
class Comment(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
	parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Comment by {self.author.username} on {self.question.title}'


