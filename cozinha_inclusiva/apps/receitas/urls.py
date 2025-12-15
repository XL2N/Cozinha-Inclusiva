from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('gerenciar_receitas/', views.gerenciar_receitas, name='gerenciar_receitas'),
]