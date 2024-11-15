from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  
from django.contrib import messages 
from .models import * 
from .forms import *


# Create your views here.
def inscription(request):
	if request.method == 'POST':
		form = UserInscriptionForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username') 
			messages.success(request, f'Votre compte a été créé, vous pouvez désormais vous connecter! { username }')
			return redirect('connexion')
	else:
		form = UserInscriptionForm()
	return render(request, "utilisateurs/inscription.html", {'form': form})


@login_required
def profil(request):
	current_user = request.user 
	if request.method == 'POST':
		user_form = UserModificationForm(request.POST, instance=current_user)
		profil_form = ProfilForm(request.POST, request.FILES, instance=current_user.profil)

		if user_form.is_valid() and profil_form.is_valid():
			user_form.save()
			profil_form.save()
			messages.success(request, 'Votre compte a été mis à jour!')
			return redirect('profil') 
	else:
		user_form = UserModificationForm(instance=current_user)
		profil_form = ProfilForm(instance=current_user.profil)

	context = {
		'title': 'Profil',
		'user_form': user_form, 
		'profil_form': profil_form
	}
	return render(request, 'utilisateurs/profil.html', context)


