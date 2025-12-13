from django.urls import path
from . import views

urlpatterns = [
    # Barra de navegação
    path('', views.home_adm, name='home_adm'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
