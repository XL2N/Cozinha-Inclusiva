from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from apps.receitas.models import Receita
from apps.categorias.models import Categoria
from .forms import BuscaForm

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

# Receita Selecionada view
def receita_selecionada(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)

    # Incrementa o contador de visualizações
    receita.visualizacoes += 1
    receita.save()

    context = {
        'receita': receita,
    }

    return render(request, 'website/receita.html', context)

# Categorias view
def categorias(request):
    categorias = Categoria.objects.annotate(num_receitas=Count('receitas')).order_by('nome')

    context = {
        'categorias': categorias,
    }

    return render(request, 'website/categoria.html', context)

# Categoria Selecionada view
def categoria_selecionada(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    receitas = Receita.objects.filter(categoria=categoria)

    context = {
        'categoria': categoria,
        'receitas': receitas,
    }

    return render(request, 'website/categoria_selecionada.html', context)

# Sobre view
def sobre(request):
    return render(request, 'website/sobre.html')

def busca(request):
    form = BuscaForm(request.GET or None)
    receitas = []
    termo = ''
    
    if form.is_valid():
        termo = form.cleaned_data.get('termo', '').strip()
        
        if termo:
            # Busca por título da receita, ingredientes e categoria
            receitas = Receita.objects.filter(
                Q(titulo__icontains=termo) |
                Q(ingredientes__nome__icontains=termo) |
                Q(categoria__nome__icontains=termo) |
                Q(descricao__icontains=termo) 
            ).distinct().order_by('-visualizacoes')

    context = {
        'form': form,
        'receitas': receitas,
        'termo': termo,
        'total': receitas.count() if receitas else 0,
    }

    return render(request, 'website/busca.html', context)

# Login, Logout e Cadastro de Usuário views
def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('inicio')

def cadastro_user(request):
    return render(request, 'cadastro.html')

