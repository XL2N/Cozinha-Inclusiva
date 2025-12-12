from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from apps.receitas.models import Receita
from apps.categorias.models import Categoria

# Create your views here.

def home(request):
    # Busca as receitas mais vistas
    queryset = Receita.objects.all().order_by('-visualizacoes')

    filtro_nome = request.GET.get('filtro')

    if filtro_nome:
        queryset = queryset.filter(categoria__nome__iexact=filtro_nome)

    categorias = Categoria.objects.all().order_by('nome')

    context = {
        'receitas': queryset[:6],  
        'categorias': categorias,
        'filtro_ativo': filtro_nome,
    }

    return render(request, 'website/inicio.html', context)

