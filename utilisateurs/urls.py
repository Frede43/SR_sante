from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import *  

urlpatterns =[
    path('profil/', profil, name='profil'),
    path('inscription/', inscription, name='inscription'), 
    path('connexion/', auth_views.LoginView.as_view(template_name='utilisateurs/connexion.html'), name='connexion'),
    path('deconnexion/', auth_views.LogoutView.as_view(template_name='utilisateurs/deconnexion.html'), name='deconnexion'),
]


