from django.urls import path, include
from . import views

urlpatterns = [
    # Telas principais do administrativo
    path('home/', views.home_adm, name='home_adm'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Ações de receitas
    path('receita/editar/<int:receita_id>/', views.editar_receita_rapido, name='editar_receita_rapido'),
    path('receita/excluir/<int:receita_id>/', views.excluir_receita, name='excluir_receita'),

    # Includes das apps administrativas
    path('categorias/', include('apps.categorias.urls')),
    path('comentarios/', include('apps.comentarios.urls')),
    path('receitas/', include('apps.receitas.urls')),
    
]
