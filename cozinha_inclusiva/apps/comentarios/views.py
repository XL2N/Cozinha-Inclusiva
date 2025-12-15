from django.shortcuts import render

# Create your views here.
def gerenciar_comentarios(request):
    return render(request, 'comentarios/gerenciar_comentarios.html')