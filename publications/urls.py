from django.urls import path
from .views import *


urlpatterns = [
	path('', publication_liste, name='publication_liste'),
	path('p/detail/<str:titre>/', publication_detail, name='publication_detail'),
	path('p/<str:post_pk>/commentaire-modifier/<str:comment_pk>/', commentaire_modifier, name='commentaire_modifier'),
	path('p/commentaire-supprimer/<str:pk>/', commentaire_supprimer, name='commentaire_supprimer'),

]


