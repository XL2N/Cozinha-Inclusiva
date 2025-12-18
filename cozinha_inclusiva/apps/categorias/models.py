from django.db import models
from django.db.models import Sum
from apps.receitas.models import Receita

# Create your models here.
class Categoria(models.Model):

    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    data_criacao = models.DateField(auto_now_add=True, verbose_name="Data de Criação")
    
    receita_mais_popular = models.ForeignKey(
        Receita,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categoria_mais_popular_vinculada', 
        verbose_name="Receita Mais Popular"
    )

    # Relacionamento M:N com Receita, tabela CategoriaReceita
    receitas = models.ManyToManyField(
        'receitas.Receita',
        through='CategoriaReceita',
        related_name='categorias_vinculadas'
    )

    # VIZUALIZACAO_TOTAL
    @property
    def visualizacao_total(self):
        """Calcula a soma de visualizações de todas as receitas vinculadas."""
        total_views = self.receitas.aggregate(Sum('visualizacoes'))['visualizacoes__sum']
        return total_views or 0

    @property
    def curtidas_total(self):
        """Calcula a soma de curtidas de todas as receitas vinculadas à categoria."""
        total_likes = self.receitas.aggregate(Sum('curtidas'))['curtidas__sum']
        return total_likes or 0

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.nome
    
# TABELA DE LIGAÇÃO
class CategoriaReceita(models.Model):

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) 
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('categoria', 'receita'), ) 
        verbose_name = "Vínculo Categoria-Receita"
        verbose_name_plural = "Vínculos Categoria-Receita"

    def __str__(self):
        return f"{self.categoria.nome} em {self.receita.titulo}"