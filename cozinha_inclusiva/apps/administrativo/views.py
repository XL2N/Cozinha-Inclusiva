
# ------ IMPORTAÇÕES -------
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from datetime import datetime, timedelta

# JSON
import json

# Models
from django.db import models
from apps.receitas.models import Receita, Ingrediente, ReceitaIngrediente, ModoPreparo
from apps.comentarios.models import Comentario
from apps.categorias.models import Categoria


''' 
-------------------------------------------------------
            ROTAS E VIEWS DA HOME
-------------------------------------------------------

'''

# ------ TELA HOME  -------
def home_adm(request):
    receitas = Receita.objects.all().order_by('-data_publicacao')
    ingredientes = Ingrediente.objects.all().order_by('nome')
    categorias = Categoria.objects.all().order_by('nome')
    context = {
        'receitas': receitas,
        'ingredientes': ingredientes,
        'categorias': categorias,
    }
    return render(request, 'administrativo/home.html', context)


''' 
-------------------------------------------------------
                ROTAS E AÇÕES DA TELA HOME 
-------------------------------------------------------
'''

# ------ ADICIONAR RECEITA -------
@require_POST
def adicionar_receita(request):
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    imagem_capa = request.FILES.get('imagem_capa')
    ingredientes_ids = request.POST.getlist('ingredientes')
    categorias_ids = request.POST.getlist('categorias')
    passos = request.POST.getlist('modo_preparo[]')

    if not (titulo and descricao and ingredientes_ids and passos):
        messages.error(request, 'Preencha todos os campos obrigatórios.')
        return redirect('home_adm')

    # Verifica se já existe receita com o mesmo título
    if Receita.objects.filter(titulo__iexact=titulo).exists():
        messages.error(request, f'Já existe uma receita com o nome "{titulo}".')
        return redirect('home_adm')

    receita = Receita.objects.create(
        titulo=titulo,
        descricao=descricao,
        imagem_capa=imagem_capa
    )

    # Categorias
    if categorias_ids:
        receita.categoria.set(categorias_ids)

    # Ingredientes (com quantidade e unidade)
    for ingrediente_id in ingredientes_ids:
        quantidade = request.POST.get(f'quantidade_{ingrediente_id}', '')
        unidade = request.POST.get(f'unidade_{ingrediente_id}', '')
        ReceitaIngrediente.objects.create(
            receita=receita,
            ingrediente_id=ingrediente_id,
            quantidade=quantidade,
            unidade_medida=unidade
        )

    # Modo de Preparo (passos)
    for idx, passo in enumerate(passos, start=1):
        if passo.strip():
            ModoPreparo.objects.create(
                receita=receita,
                num_ordem=idx,
                descricao=passo.strip()
            )

    messages.success(request, f'Receita "{titulo}" adicionada com sucesso!')
    return redirect('home_adm')

# ----- EDIÇÃO RÁPIDA DE RECEITA  -------

def editar_receita_rapido(request, receita_id):
    """Edição rápida de título e descrição da receita"""
    receita = get_object_or_404(Receita, id=receita_id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        
        if titulo and descricao:
            # Verificar se já existe outra receita com o mesmo título
            receita_existente = Receita.objects.filter(titulo__iexact=titulo).exclude(id=receita_id).first()
            
            if receita_existente:
                messages.error(request, f'Já existe uma receita com o nome "{titulo}". Por favor, escolha outro nome.')
            else:
                receita.titulo = titulo
                receita.descricao = descricao
                receita.save()
                
                messages.success(request, f'Receita "{titulo}" editada com sucesso!')
        else:
            messages.error(request, 'Todos os campos são obrigatórios.')
        
        return redirect('home_adm')
    
    return redirect('home_adm')

# ----- EXCLUSÃO DE RECEITA  -------
def excluir_receita(request, receita_id):
    """Exclusão de receita"""
    receita = get_object_or_404(Receita, id=receita_id)
    
    if request.method == 'POST':
        titulo_receita = receita.titulo
        receita.delete()
        messages.success(request, f'Receita "{titulo_receita}" excluída com sucesso!')
        return redirect('home_adm')
    
    return redirect('home_adm')

'''
-------------------------------------------------------
            ROTA E AÇÕES DA TELA DASHBOARD
-------------------------------------------------------
'''

# ----- TELA DASHBOARD  -------

def dashboard(request):
    # Filtros
    filtro_data = request.GET.get('filtro_data', 'mes')
    filtro_categoria = request.GET.get('filtro_categoria', '')

    receitas = Receita.objects.all()

    # Filtro de data
    hoje = datetime.now()
    if filtro_data == 'semana':
        inicio = hoje - timedelta(days=7)
        receitas = receitas.filter(data_publicacao__gte=inicio)
    elif filtro_data == 'mes':
        inicio = hoje - timedelta(days=30)
        receitas = receitas.filter(data_publicacao__gte=inicio)
    elif filtro_data == 'ano':
        inicio = hoje - timedelta(days=365)
        receitas = receitas.filter(data_publicacao__gte=inicio)
    # 'tudo' não filtra

    # Filtro de categoria
    if filtro_categoria:
        receitas = receitas.filter(categoria__id=filtro_categoria)

    categorias = Categoria.objects.all().order_by('nome')

    # Total de visualizações das receitas filtradas
    total_visualizacoes = receitas.aggregate(total=models.Sum('visualizacoes'))['total'] or 0

    # Total de comentários (pode ser filtrado por receitas exibidas)
    total_comentarios = Comentario.objects.filter(receita__in=receitas).count()

    # Geração de dados para o gráfico de visualizações por dia (últimos 30 dias)
    dias = []
    visualizacoes_por_dia = []
    for i in range(29, -1, -1):
        dia = (datetime.now() - timedelta(days=i)).date()
        dias.append(dia.strftime('%d/%m'))
        visualizacoes = receitas.filter(data_publicacao__date=dia).aggregate(total=models.Sum('visualizacoes'))['total'] or 0
        visualizacoes_por_dia.append(visualizacoes)


    # Gráfico de pizza: categorias mais curtidas (soma das curtidas das receitas de cada categoria)
    categorias_curtidas = (
        categorias.annotate(total_curtidas=models.Sum('receitas_categoria__curtidas'))
        .order_by('-total_curtidas')[:5]
    )
    grafico_curtidas_labels = [c.nome for c in categorias_curtidas]
    grafico_curtidas_dados = [c.total_curtidas or 0 for c in categorias_curtidas]

    context = {
        'receitas': receitas.order_by('-data_publicacao'),
        'categorias': categorias,
        'filtro_data': filtro_data,
        'filtro_categoria': filtro_categoria,
        'total_visualizacoes': total_visualizacoes,
        'total_comentarios': total_comentarios,
        'grafico_labels': json.dumps(dias),
        'grafico_dados': json.dumps(visualizacoes_por_dia),
        'grafico_curtidas_labels': json.dumps(grafico_curtidas_labels, ensure_ascii=False),
        'grafico_curtidas_dados': json.dumps(grafico_curtidas_dados),
    }
    return render(request, 'administrativo/dashboard.html', context)
