from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
ROLE_CHOICES = (
	("membre", "membre"),
	("partenaire", "partenaire"),
)

class Profil(models.Model):
	utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
	nom_complet = models.CharField(max_length=200, blank=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='images/', blank=True, null=True)
	role = models.CharField(max_length=50, blank=True, null=True, choices=ROLE_CHOICES)

	def __str__(self):
		return self.utilisateur.username

	def get_absolute_url(self):
		return reverse('profil_detail', args=[self.pk])


@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
	if created:
		Profil.objects.create(utilisateur=instance)
	else: 
		instance.profil.save()






