from django.shortcuts import render

# Create your views here.
def gerenciar_receitas(request):
    return render(request, 'receitas/gerenciar_receitas.html')