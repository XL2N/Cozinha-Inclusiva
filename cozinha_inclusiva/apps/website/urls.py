from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('', views.home, name='inicio'),
    path('categorias/', views.categorias, name='categorias'),
    path('sobre/', views.sobre, name='sobre'),
    path('busca/', views.busca, name='busca'),

    # Páginas de conteúdo selecionado   
    path('receita/<int:receita_id>/', views.receita_selecionada, name='receita_selecionada'),
    path('categoria/<int:categoria_id>/', views.categoria_selecionada, name='categoria_selecionada'),
]
