from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('gerenciar_receitas/', views.gerenciar_receitas, name='gerenciar_receitas'),
    path('adicionar_receita/', views.adicionar_receita, name='adicionar_receita'),
    path('editar_receita/<int:receita_id>/', views.editar_receita, name='editar_receita'),
    path('excluir_receita/<int:receita_id>/', views.excluir_receita, name='excluir_receita'),
]