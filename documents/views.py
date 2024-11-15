from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def document_liste(request):
	documents = Document.objects.all()
	context = {
		'title': 'Documents liste',
		'documents': documents,
	}
	return render(request, 'documents/document_liste.html', context)

def document_detail(request, titre):
	document = get_object_or_404(Document, titre=titre)
	context = {
		'title': 'Document détail',
		'document':  document,
	}
	return render(request, 'documents/document_detail.html', context)



