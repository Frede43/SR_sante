from django.urls import path
from .views import *


urlpatterns = [
	path('liste/', partenaire_liste, name='partenaire_liste'),
	path('detail/<str:nom>/', partenaire_detail, name='partenaire_detail'),
]

