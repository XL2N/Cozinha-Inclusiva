from django.urls import path, include
from . import views

urlpatterns = [
    # Telas principais do administrativo
    path('', views.home_adm, name='home_adm'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Includes das apps administrativas
    path('', include('apps.website.urls')),
    path('categorias/', include('apps.categorias.urls')),
    path('comentarios/', include('apps.comentarios.urls')),
    path('receitas/', include('apps.receitas.urls')),
]
