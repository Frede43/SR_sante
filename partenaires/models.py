from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Partenaire(models.Model):
	nom = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	logo = models.ImageField(upload_to='images/', blank=True, null=True)
	email = models.EmailField(max_length=100, blank=True,)
	siteweb = models.URLField(max_length=100, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.nom

	def get_absolute_url(self):
		return reverse('partenaire_detail', args=[self.nom])

