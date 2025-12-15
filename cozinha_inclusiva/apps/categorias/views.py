from django.shortcuts import render

# Create your views here.
def gerenciar_categorias(request):
    return render(request, 'categorias/gerenciar_categorias.html')