from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required 
from django.urls import reverse, reverse_lazy  
from django.core.paginator import Paginator
from django.db.models import Q 
from .models import * 
from .forms import *

# Create your views here.
def publication_liste(request):
	search = request.GET.get('search') or ""

	publications = Publication.objects.filter(
		Q(utilisateur__username__icontains=search)|
		Q(utilisateur__email__icontains=search)|
		Q(titre__icontains=search)|
		Q(created__icontains=search)
	)

	context = {
		'title': 'Publications liste',
		"search":search,
		'publications': publications,
	}
	return render(request, 'publications/publication_liste.html', context)


def publication_detail(request, titre):
	publication = get_object_or_404(Publication, titre=titre)

	if request.user.is_authenticated and request.method == 'POST':
		comment_form = CommentaireForm(request.POST)

		if comment_form.is_valid():
			instance = comment_form.save(commit=False)
			instance.publication = publication 
			instance.utilisateur = request.user
			instance.save()
			return redirect(publication.get_absolute_url())
	else:
		comment_form = CommentaireForm()

	context = {
		'title': 'Publication détail',
		'publication':  publication,
		'comment_form':  comment_form,
	}
	return render(request, 'publications/publication_detail.html', context)


@login_required
def commentaire_modifier(request, post_pk, comment_pk):
	publication = get_object_or_404(Publication, pk=post_pk)
	commentaire = get_object_or_404(Commentaire, pk=comment_pk)

	if request.method == 'POST':
		comment_form = CommentForm(request.POST, instance=commentaire) 
		if comment_form.is_valid():
			comment_form.save()
			return redirect(commentaire.post.get_absolute_url())
	else:
		comment_form = CommentForm(instance=commentaire) 

	context = {
		'post':post,
		'comment_form':comment_form,
	}
	return render(request, 'publications/publication_detail.html', context)


@login_required
def commentaire_supprimer(request, pk):
	commentaire = Commentaire.objects.get(pk=pk, utilisateur=request.user)
	commentaire.delete()
	messages.success(request, 'Votre commentaire a été supprimé!')
	return redirect(commentaire.post.get_absolute_url())


