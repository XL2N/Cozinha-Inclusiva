from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('gerenciar_categorias/', views.gerenciar_categorias, name='gerenciar_categorias'),
    path('adicionar_categoria/', views.adicionar_categoria, name='adicionar_categoria'),
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('excluir_categorias/', views.excluir_categorias, name='excluir_categorias'),
    path('buscar_receitas/', views.buscar_receitas, name='buscar_receitas'),
]