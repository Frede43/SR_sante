from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from partenaires.models import Partenaire

# Create your models here.
class Publication(models.Model):
	utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
	titre = models.CharField(max_length=200, blank=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='post_images/', blank=True, null=True)
	partenaires = models.ManyToManyField(Partenaire, related_name='partenaires', blank=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.utilisateur.username

	def get_absolute_url(self):
		return reverse('publication_detail', args=[self.titre])


class Commentaire(models.Model):
	utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='commentaires')
	description = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.utilisateur.username


