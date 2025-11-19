from django.db import models

# Create your models here.
class Categoria(models.Model):

    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    visualizacoes = models.IntegerField(default=0)
    receita_popular = models.BooleanField(default=False, verbose_name="É Receita Popular")
    receitas_vinculadas = models.IntegerField(default=0)
    data_criacao = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.nome