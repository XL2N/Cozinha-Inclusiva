from django.contrib import admin
from .models import Comentario, PalavraBloqueada

# Register your models here.
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'receita', 'texto', 'data_hora')
    list_filter = ('data_hora',)
    search_fields = ('texto', 'usuario__username', 'receita__titulo')
    date_hierarchy = 'data_hora'

@admin.register(PalavraBloqueada)
class PalavraBloqueadaAdmin(admin.ModelAdmin):
    list_display = ('palavra', 'data_criacao')
    search_fields = ('palavra',)
    date_hierarchy = 'data_criacao'
