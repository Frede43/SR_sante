from django.urls import path
from .views import *


urlpatterns = [
	path('liste/', document_liste, name='document_liste'),
	path('detail/<str:titre>/', document_detail, name='document_detail'),
]

