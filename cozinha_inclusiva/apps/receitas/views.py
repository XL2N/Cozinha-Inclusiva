from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta

from apps.receitas.models import Receita
from apps.categorias.models import Categoria

# Create your views here.
def gerenciar_receitas(request):
    # Filtros
    categoria_id = request.GET.get('categoria', '')
    periodo = request.GET.get('periodo', '')
    termo_busca = request.GET.get('q', '').strip()

    receitas = Receita.objects.all()

    # Filtro por categoria
    if categoria_id:
        receitas = receitas.filter(categoria__id=categoria_id)

    # Filtro por período
    if periodo == '7':
        receitas = receitas.filter(data_publicacao__gte=datetime.now() - timedelta(days=7))
    elif periodo == '30':
        receitas = receitas.filter(data_publicacao__gte=datetime.now() - timedelta(days=30))

    # Filtro por termo de busca
    if termo_busca:
        receitas = receitas.filter(
            Q(titulo__icontains=termo_busca) |
            Q(descricao__icontains=termo_busca) |
            Q(receitaingrediente__ingrediente__nome__icontains=termo_busca)
        ).distinct()

    # Paginação
    paginator = Paginator(receitas.order_by('-data_publicacao'), 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    context = {
        'receitas': page_obj,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'periodo_selecionado': periodo,
        'termo_busca': termo_busca,
    }

    return render(request, 'receitas/gerenciar_receitas.html', context)