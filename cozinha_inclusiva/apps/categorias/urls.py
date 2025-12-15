from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('gerenciar_categorias/', views.gerenciar_categorias, name='gerenciar_categorias'),
]