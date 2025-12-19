from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from apps.comentarios.models import Comentario, PalavraBloqueada

# Create your views here.
def gerenciar_comentarios(request):
    # Filtros
    periodo = request.GET.get('periodo', '')
    termo_busca = request.GET.get('q', '').strip()

    comentarios = Comentario.objects.select_related('usuario', 'receita').all()

    # Filtro por período
    if periodo == '7':
        comentarios = comentarios.filter(data_hora__gte=datetime.now() - timedelta(days=7))
    elif periodo == '30':
        comentarios = comentarios.filter(data_hora__gte=datetime.now() - timedelta(days=30))

    # Filtro por termo de busca
    if termo_busca:
        comentarios = comentarios.filter(
            Q(texto__icontains=termo_busca) |
            Q(receita__titulo__icontains=termo_busca) |
            Q(usuario__username__icontains=termo_busca)
        )

    # Paginação
    paginator = Paginator(comentarios, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'comentarios': page_obj,
        'periodo_selecionado': periodo,
        'termo_busca': termo_busca,
    }

    return render(request, 'comentarios/gerenciar_comentarios.html', context)


def excluir_comentario(request, comentario_id):
    if request.method == 'POST':
        try:
            comentario = get_object_or_404(Comentario, id=comentario_id)
            usuario_nome = comentario.usuario.username if comentario.usuario else "Usuário Deletado"
            comentario.delete()
            messages.success(request, f'Comentário de "{usuario_nome}" excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir comentário: {str(e)}')
    
    return redirect('gerenciar_comentarios')


def moderacao_palavras(request):
    if request.method == 'POST':
        try:
            # Adicionar nova palavra
            palavra = request.POST.get('palavra', '').strip().lower()
            if palavra:
                PalavraBloqueada.objects.get_or_create(palavra=palavra)
                messages.success(request, f'Palavra "{palavra}" adicionada à lista de bloqueio!')
        except Exception as e:
            messages.error(request, f'Erro ao adicionar palavra: {str(e)}')
        
        return redirect('gerenciar_comentarios')
    
    # GET - retornar lista de palavras bloqueadas
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        palavras = list(PalavraBloqueada.objects.values('id', 'palavra'))
        return JsonResponse({'palavras': palavras})
    
    return redirect('gerenciar_comentarios')


def remover_palavra_bloqueada(request, palavra_id):
    if request.method == 'POST':
        try:
            palavra = get_object_or_404(PalavraBloqueada, id=palavra_id)
            palavra_texto = palavra.palavra
            palavra.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Palavra "{palavra_texto}" removida!'})
            
            messages.success(request, f'Palavra "{palavra_texto}" removida da lista de bloqueio!')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            messages.error(request, f'Erro ao remover palavra: {str(e)}')
    
    return redirect('gerenciar_comentarios')


def salvar_moderacao(request):
    if request.method == 'POST':
        messages.success(request, 'Configurações de moderação salvas com sucesso!')
    return redirect('gerenciar_comentarios')