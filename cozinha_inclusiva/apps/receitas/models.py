from django.db import models
from django.db.models import Sum

# ENTIDADE RECEITA.
class Receita(models.Model):

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(verbose_name="Descrição")
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")
    visualizacoes = models.IntegerField(default=0, verbose_name="Visualizações")
    imagem_capa = models.ImageField(upload_to='receitas/capas/', blank=True, null=True, verbose_name="Imagem de Capa")
    referencia = models.URLField(max_length=500, blank=True, null=True, verbose_name="Referência")

    # Relacionamento M:N com Ingrediente, tabela ReceitaIngrediente
    ingredientes = models.ManyToManyField(
        'Ingrediente',
        through='ReceitaIngrediente',
        related_name='receitas_usando',
    )

    categoria = models.ManyToManyField(
        'categorias.Categoria',  # Referência como string 'app_name.ModelName'
        related_name='receitas_categoria'
    )

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"

    def __str__(self):
        return self.titulo
    
# ENTIDADE INGREDIENTE
class Ingrediente(models.Model):

    nome = models.CharField(
        max_length = 100,
        unique = True,
        verbose_name = "Nome"
    )

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
    
    def __str__(self):
        return self.nome
    
# TABELA RECEITA_INGREDIENTE

class ReceitaIngrediente(models.Model):

    receita = models.ForeignKey( Receita, on_delete = models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.CharField(max_length=50, verbose_name="Quantidade")
    unidade_medida = models.CharField(max_length=50, verbose_name="Unidade de Medida")

    class Meta:
        unique_together = (('receita', 'ingrediente'),)
        verbose_name = "Ingrediente da Receita"
        verbose_name_plural = "Ingredientes da Receita"

    def __str__(self):
        return f"{self.quantidade} de {self.ingrediente.nome} em {self.receita.titulo}"
    
# ENTIDADE MODO_PREPARO
class ModoPreparo(models.Model):

    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='passos', verbose_name="Receita")
    num_ordem = models.IntegerField(verbose_name="Número do Passo")
    descricao = models.TextField(verbose_name="Descrição do Passo")

    class Meta:
        verbose_name = "Modo de Preparo"
        unique_together = (('receita', 'num_ordem'),)
        ordering = ['num_ordem']

    def __str__(self):
        return f"Passo {self.num_ordem} de {self.receita.titulo}"