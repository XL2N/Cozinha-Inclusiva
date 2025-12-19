from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Categoria, CategoriaReceita
from apps.receitas.models import Receita

# Create your views here.
def gerenciar_categorias(request):
    categorias = Categoria.objects.annotate(
        total_receitas=Count('receitas', distinct=True)
    ).order_by('-data_criacao')
    
    receitas = Receita.objects.all().order_by('titulo')
    
    context = {
        'categorias': categorias,
        'receitas': receitas,
    }
    return render(request, 'categorias/gerenciar_categorias.html', context)


def adicionar_categoria(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome', '').strip()
            receitas_ids = request.POST.getlist('receitas')
            
            if not nome:
                messages.error(request, 'Nome da categoria é obrigatório!')
                return redirect('gerenciar_categorias')
            
            # Criar categoria
            categoria = Categoria.objects.create(nome=nome)
            
            # Vincular receitas selecionadas
            if receitas_ids:
                for receita_id in receitas_ids:
                    receita = Receita.objects.get(id=receita_id)
                    CategoriaReceita.objects.create(categoria=categoria, receita=receita)
                
                # Definir receita mais popular (a com mais visualizações)
                receita_popular = Receita.objects.filter(id__in=receitas_ids).order_by('-visualizacoes').first()
                if receita_popular:
                    categoria.receita_mais_popular = receita_popular
                    categoria.save()
            
            messages.success(request, f'Categoria "{nome}" criada com sucesso!')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar categoria: {str(e)}')
    
    return redirect('gerenciar_categorias')


def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome', '').strip()
            receitas_ids = request.POST.getlist('receitas')
            
            if not nome:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Nome da categoria é obrigatório!'})
                messages.error(request, 'Nome da categoria é obrigatório!')
                return redirect('gerenciar_categorias')
            
            # Atualizar nome
            categoria.nome = nome
            
            # Atualizar vínculos de receitas
            CategoriaReceita.objects.filter(categoria=categoria).delete()
            
            if receitas_ids:
                for receita_id in receitas_ids:
                    receita = Receita.objects.get(id=receita_id)
                    CategoriaReceita.objects.create(categoria=categoria, receita=receita)
                
                # Atualizar receita mais popular
                receita_popular = Receita.objects.filter(id__in=receitas_ids).order_by('-visualizacoes').first()
                if receita_popular:
                    categoria.receita_mais_popular = receita_popular
            else:
                categoria.receita_mais_popular = None
            
            categoria.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Categoria "{nome}" atualizada com sucesso!'})
            
            messages.success(request, f'Categoria "{nome}" atualizada com sucesso!')
            return redirect('gerenciar_categorias')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': f'Erro ao atualizar categoria: {str(e)}'})
            messages.error(request, f'Erro ao atualizar categoria: {str(e)}')
            return redirect('gerenciar_categorias')
    
    # GET - retornar dados da categoria em JSON
    try:
        receitas_vinculadas = categoria.receitas.all()
        
        receitas_data = []
        for receita in receitas_vinculadas:
            # Obter URL da imagem de forma segura
            imagem_url = None
            try:
                if receita.capa and hasattr(receita.capa, 'url'):
                    imagem_url = receita.capa.url
            except:
                imagem_url = None
            
            receitas_data.append({
                'id': receita.id,
                'titulo': receita.titulo,
                'imagem_url': imagem_url,
            })
        
        data = {
            'id': categoria.id,
            'nome': categoria.nome,
            'receitas_ids': [r.id for r in receitas_vinculadas],
            'receitas': receitas_data,
        }
        return JsonResponse(data)
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Erro ao carregar categoria: {error_detail}")
        return JsonResponse({'error': str(e), 'detail': error_detail}, status=500)


def excluir_categorias(request):
    if request.method == 'POST':
        try:
            # Tentar pegar o campo como string e dividir por vírgula
            categorias_ids_str = request.POST.get('categorias_ids', '')
            if categorias_ids_str:
                categorias_ids = categorias_ids_str.split(',')
            else:
                categorias_ids = request.POST.getlist('categorias_ids[]')
            
            if not categorias_ids:
                messages.error(request, 'Nenhuma categoria selecionada!')
                return redirect('gerenciar_categorias')
            
            categorias = Categoria.objects.filter(id__in=categorias_ids)
            count = categorias.count()
            categorias.delete()
            
            messages.success(request, f'{count} categoria(s) excluída(s) com sucesso!')
            
        except Exception as e:
            messages.error(request, f'Erro ao excluir categorias: {str(e)}')
    
    return redirect('gerenciar_categorias')


def buscar_receitas(request):
    """Endpoint para buscar receitas via AJAX"""
    query = request.GET.get('q', '').strip()
    
    if query:
        receitas = Receita.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        )[:20]
    else:
        receitas = Receita.objects.all()[:20]
    
    data = {
        'receitas': [
            {
                'id': r.id,
                'titulo': r.titulo,
                'descricao': r.descricao[:100] + '...' if len(r.descricao) > 100 else r.descricao,
                'imagem_url': r.imagem_capa.url if r.imagem_capa else None
            }
            for r in receitas
        ]
    }
    
    return JsonResponse(data)