from django.shortcuts import render

# Create your views here.
from .models import Categoria

def gerenciar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/gerenciar_categorias.html', {'categorias': categorias})