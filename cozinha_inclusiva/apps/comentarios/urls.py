from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('gerenciar_comentarios/', views.gerenciar_comentarios, name='gerenciar_comentarios'),
]