from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib import messages
from apps.receitas.models import Receita
from apps.categorias.models import Categoria
from apps.comentarios.models import Comentario
from .forms import BuscaForm, ComentarioForm

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

    # Processar formulário de comentário
    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.receita = receita
            comentario.usuario = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('receita_selecionada', receita_id=receita.id)
    else:
        form = ComentarioForm()

    # Buscar comentários da receita
    comentarios = receita.comentarios.all().order_by('-data_hora')

    context = {
        'receita': receita,
        'comentarios': comentarios,
        'form': form,
        'total_comentarios': comentarios.count(),
    }

    return render(request, 'website/receita.html', context)

# Categorias view
def categorias(request):
    categorias = Categoria.objects.annotate(num_receitas=Count('receitas_categoria')).order_by('nome')

    context = {
        'categorias': categorias,
    }

    return render(request, 'website/categoria.html', context)

# Categoria Selecionada view
def categoria_selecionada(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    receitas_list = Receita.objects.filter(categoria=categoria).order_by('-id')
    
    # Paginação - 8 receitas por página
    paginator = Paginator(receitas_list, 8)
    page_number = request.GET.get('page', 1)
    receitas = paginator.get_page(page_number)
    
    # Contagem total de receitas
    total_receitas = receitas_list.count()

    context = {
        'categoria': categoria,
        'receitas': receitas,
        'total_receitas': total_receitas,
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