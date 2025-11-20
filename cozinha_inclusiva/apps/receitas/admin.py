from django.contrib import admin
from .models import Receita, Ingrediente, ReceitaIngrediente, ModoPreparo

# TABELA RECEITA_INGREDIENTE
class ReceitaIngredienteInline(admin.TabularInline):
    model = ReceitaIngrediente
    fields = ['ingrediente', 'quantidade', 'unidade_medida'] 
    extra = 1

# TABELA MODO_PREPARO
class ModoPreparoInline(admin.TabularInline):
    model = ModoPreparo
    fields = ['num_ordem', 'descricao']
    extra = 1
    ordering = ['num_ordem']

# TABELA RECEITAS
@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    # Campos exibidos
    list_display = (
        'titulo', 
        'data_publicacao', 
        'visualizacoes', 
        'display_categorias'
    )

    # Campos que podem ser usados para buscar receitas
    search_fields = ('titulo', 'ingredientes__nome', 'categoria__nome') 
    # Campos que podem ser usados para filtrar a lista
    list_filter = ('data_publicacao', 'categoria')
    # Adiciona os inlines para gerenciamento M:N e 1:N
    inlines = [ReceitaIngredienteInline, ModoPreparoInline]
    
    # Exibe as categorias na list_display
    def display_categorias(self, obj):
        return ", ".join([cat.nome for cat in obj.categoria.all()[:3]])
    
    display_categorias.short_description = 'Categorias'

# TABELA INGREDIENTES
@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de ingredientes
    list_display = ('nome',)
    search_fields = ('nome',)