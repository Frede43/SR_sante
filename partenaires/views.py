from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def partenaire_liste(request):
	partenaires = Partenaire.objects.all()
	context = {
		'title': 'Partenaires liste',
		'partenaires': partenaires,
	}
	return render(request, 'partenaires/partenaire_liste.html', context)

def partenaire_detail(request, nom):
	partenaire = get_object_or_404(Partenaire, nom=nom)
	context = {
		'title': 'Partenaire détail',
		'partenaire':  partenaire,
	}
	return render(request, 'partenaires/partenaire_detail.html', context)



