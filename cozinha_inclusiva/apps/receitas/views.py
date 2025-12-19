from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta

from apps.receitas.models import Receita, Ingrediente, ReceitaIngrediente, ModoPreparo
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
    ingredientes = Ingrediente.objects.all().order_by('nome')

    context = {
        'receitas': page_obj,
        'categorias': categorias,
        'ingredientes': ingredientes,
        'categoria_selecionada': categoria_id,
        'periodo_selecionado': periodo,
        'termo_busca': termo_busca,
    }

    return render(request, 'receitas/gerenciar_receitas.html', context)


def adicionar_receita(request):
    if request.method == 'POST':
        try:
            # Dados básicos da receita
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')
            referencia = request.POST.get('referencia', '')
            imagem_capa = request.FILES.get('imagem_capa')
            
            # Restrições alimentares
            sem_lactose = request.POST.get('sem_lactose') == 'on'
            sem_gluten = request.POST.get('sem_gluten') == 'on'
            vegano = request.POST.get('vegano') == 'on'
            vegetariano = request.POST.get('vegetariano') == 'on'

            # Criar a receita
            receita = Receita.objects.create(
                titulo=titulo,
                descricao=descricao,
                referencia=referencia,
                imagem_capa=imagem_capa,
                sem_lactose=sem_lactose,
                sem_gluten=sem_gluten,
                vegano=vegano,
                vegetariano=vegetariano
            )

            # Adicionar categorias
            categorias_ids = request.POST.getlist('categorias')
            if categorias_ids:
                receita.categoria.set(categorias_ids)

            # Adicionar ingredientes
            ingredientes_ids = request.POST.getlist('ingredientes')
            for ingrediente_id in ingredientes_ids:
                quantidade = request.POST.get(f'quantidade_{ingrediente_id}')
                unidade = request.POST.get(f'unidade_{ingrediente_id}')
                
                if quantidade and unidade:
                    ReceitaIngrediente.objects.create(
                        receita=receita,
                        ingrediente_id=ingrediente_id,
                        quantidade=quantidade,
                        unidade_medida=unidade
                    )

            # Adicionar modo de preparo
            modo_preparo_list = request.POST.getlist('modo_preparo[]')
            for ordem, descricao_passo in enumerate(modo_preparo_list, start=1):
                if descricao_passo.strip():
                    ModoPreparo.objects.create(
                        receita=receita,
                        num_ordem=ordem,
                        descricao=descricao_passo
                    )

            messages.success(request, f'Receita "{titulo}" adicionada com sucesso!')
            return redirect('gerenciar_receitas')

        except Exception as e:
            messages.error(request, f'Erro ao adicionar receita: {str(e)}')
            return redirect('gerenciar_receitas')

    return redirect('gerenciar_receitas')


def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    
    if request.method == 'POST':
        try:
            # Atualizar dados básicos
            receita.titulo = request.POST.get('titulo')
            receita.descricao = request.POST.get('descricao')
            receita.referencia = request.POST.get('referencia', '')
            
            # Atualizar imagem se fornecida
            if 'imagem_capa' in request.FILES:
                receita.imagem_capa = request.FILES.get('imagem_capa')
            
            # Restrições alimentares
            receita.sem_lactose = request.POST.get('sem_lactose') == 'on'
            receita.sem_gluten = request.POST.get('sem_gluten') == 'on'
            receita.vegano = request.POST.get('vegano') == 'on'
            receita.vegetariano = request.POST.get('vegetariano') == 'on'
            
            receita.save()

            # Atualizar categorias
            categorias_ids = request.POST.getlist('categorias')
            receita.categoria.set(categorias_ids)

            # Atualizar ingredientes - remover antigos e adicionar novos
            ReceitaIngrediente.objects.filter(receita=receita).delete()
            ingredientes_ids = request.POST.getlist('ingredientes')
            for ingrediente_id in ingredientes_ids:
                quantidade = request.POST.get(f'quantidade_{ingrediente_id}')
                unidade = request.POST.get(f'unidade_{ingrediente_id}')
                
                if quantidade and unidade:
                    ReceitaIngrediente.objects.create(
                        receita=receita,
                        ingrediente_id=ingrediente_id,
                        quantidade=quantidade,
                        unidade_medida=unidade
                    )

            # Atualizar modo de preparo
            ModoPreparo.objects.filter(receita=receita).delete()
            modo_preparo_list = request.POST.getlist('modo_preparo[]')
            for ordem, descricao_passo in enumerate(modo_preparo_list, start=1):
                if descricao_passo.strip():
                    ModoPreparo.objects.create(
                        receita=receita,
                        num_ordem=ordem,
                        descricao=descricao_passo
                    )

            messages.success(request, f'Receita "{receita.titulo}" atualizada com sucesso!')
            return redirect('gerenciar_receitas')

        except Exception as e:
            messages.error(request, f'Erro ao editar receita: {str(e)}')
            return redirect('gerenciar_receitas')

    # GET - retornar dados da receita em JSON para o modal
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        ingredientes_receita = ReceitaIngrediente.objects.filter(receita=receita)
        modo_preparo = ModoPreparo.objects.filter(receita=receita).order_by('num_ordem')
        
        data = {
            'id': receita.id,
            'titulo': receita.titulo,
            'descricao': receita.descricao,
            'referencia': receita.referencia or '',
            'sem_lactose': receita.sem_lactose,
            'sem_gluten': receita.sem_gluten,
            'vegano': receita.vegano,
            'vegetariano': receita.vegetariano,
            'categorias': list(receita.categoria.values_list('id', flat=True)),
            'ingredientes': [
                {
                    'id': ri.ingrediente.id,
                    'quantidade': ri.quantidade,
                    'unidade': ri.unidade_medida
                } for ri in ingredientes_receita
            ],
            'modo_preparo': [mp.descricao for mp in modo_preparo],
            'imagem_url': receita.imagem_capa.url if receita.imagem_capa else ''
        }
        return JsonResponse(data)

    return redirect('gerenciar_receitas')


def excluir_receita(request, receita_id):
    if request.method == 'POST':
        try:
            receita = get_object_or_404(Receita, id=receita_id)
            titulo = receita.titulo
            receita.delete()
            messages.success(request, f'Receita "{titulo}" excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir receita: {str(e)}')
    
    return redirect('gerenciar_receitas')