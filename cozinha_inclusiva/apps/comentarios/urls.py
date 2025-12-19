from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('gerenciar_comentarios/', views.gerenciar_comentarios, name='gerenciar_comentarios'),
    path('excluir_comentario/<int:comentario_id>/', views.excluir_comentario, name='excluir_comentario'),
    path('moderacao_palavras/', views.moderacao_palavras, name='moderacao_palavras'),
    path('remover_palavra_bloqueada/<int:palavra_id>/', views.remover_palavra_bloqueada, name='remover_palavra_bloqueada'),
    path('salvar_moderacao/', views.salvar_moderacao, name='salvar_moderacao'),
]