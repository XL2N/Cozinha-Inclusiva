# ------ IMPORTAÇÕES -------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.receitas.models import Receita

# ------ TELA HOME  -------
def home_adm(request):
    receitas = Receita.objects.all().order_by('-data_publicacao')
    context = {
        'receitas': receitas
    }
    return render(request, 'administrativo/home.html', context)

# ----- TELA DASHBOARD  -------
def dashboard(request):
    return render(request, 'administrativo/dashboard.html')

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