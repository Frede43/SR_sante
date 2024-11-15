from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Categorie(models.Model):
	nom = models.CharField(max_length=50, unique=True)

	class Meta:
		ordering = ('nom',)
		verbose_name = 'Catégorie'
		verbose_name_plural = 'Catégories'

	def __str__(self):
		return self.nom

class Document(models.Model):
	utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
	titre = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	fichier = models.FileField(upload_to='docs/', blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.titre

	def get_absolute_url(self):
		return reverse('document_detail', args=[self.titre])


