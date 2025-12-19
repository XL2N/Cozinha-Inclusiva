
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
    from django.db.models import Count
    from collections import defaultdict
    import calendar
    
    # Filtros de data
    data_inicio_str = request.GET.get('data_inicio', '')
    data_fim_str = request.GET.get('data_fim', '')
    
    # Datas padrão
    hoje = datetime.now().date()
    if not data_inicio_str:
        data_inicio = hoje - timedelta(days=30)
    else:
        data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
    
    if not data_fim_str:
        data_fim = hoje
    else:
        data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
    
    # Estatísticas gerais
    total_receitas = Receita.objects.all().count()
    total_categorias = Categoria.objects.all().count()
    total_visualizacoes = Receita.objects.aggregate(total=models.Sum('visualizacoes'))['total'] or 0
    total_comentarios = Comentario.objects.all().count()
    
    # Top 5 receitas mais visualizadas
    top_receitas_visualizacoes = Receita.objects.all().order_by('-visualizacoes')[:5]
    grafico_receitas_labels = [r.titulo for r in top_receitas_visualizacoes]
    grafico_receitas_dados = [r.visualizacoes for r in top_receitas_visualizacoes]
    
    # Quantidade de receitas por categoria
    categorias = Categoria.objects.all()
    categorias_count = categorias.annotate(total_receitas=Count('receitas')).order_by('-total_receitas')
    grafico_categorias_labels = [c.nome for c in categorias_count]
    grafico_categorias_dados = [c.total_receitas for c in categorias_count]
    total_receitas_categorias = sum(grafico_categorias_dados)
    
    # Calendário de publicações (mês atual)
    mes_atual = hoje.month
    ano_atual = hoje.year
    cal = calendar.monthcalendar(ano_atual, mes_atual)
    mes_nome = calendar.month_name[mes_atual]
    
    # Dias com publicações
    receitas_mes = Receita.objects.filter(
        data_publicacao__year=ano_atual,
        data_publicacao__month=mes_atual
    )
    dias_publicacao = set(receitas_mes.values_list('data_publicacao__day', flat=True))
    
    # Ranking de receitas mais comentadas
    receitas_mais_comentadas = Receita.objects.annotate(
        total_comentarios=Count('comentarios')
    ).filter(total_comentarios__gt=0).order_by('-total_comentarios')[:3]
    
    # Preparar dados do calendário
    calendario_semanas = []
    for semana in cal:
        semana_dias = []
        for dia in semana:
            if dia == 0:
                semana_dias.append({'dia': '', 'publicado': False})
            else:
                semana_dias.append({'dia': dia, 'publicado': dia in dias_publicacao})
        calendario_semanas.append(semana_dias)
    
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_receitas': total_receitas,
        'total_categorias': total_categorias,
        'total_visualizacoes': total_visualizacoes,
        'total_comentarios': total_comentarios,
        'grafico_receitas_labels': json.dumps(grafico_receitas_labels, ensure_ascii=False),
        'grafico_receitas_dados': json.dumps(grafico_receitas_dados),
        'grafico_categorias_labels': json.dumps(grafico_categorias_labels, ensure_ascii=False),
        'grafico_categorias_dados': json.dumps(grafico_categorias_dados),
        'total_receitas_categorias': total_receitas_categorias,
        'calendario_semanas': calendario_semanas,
        'mes_nome': mes_nome,
        'ano_atual': ano_atual,
        'receitas_mais_comentadas': receitas_mais_comentadas,
        'categorias': categorias,
    }
    return render(request, 'administrativo/dashboard.html', context)
