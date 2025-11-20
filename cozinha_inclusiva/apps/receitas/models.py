from django.db import models
from apps.categorias.models import Categoria

# Models RECEITA.
class Receita(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    ingredientes = models.TextField()
    modo_preparo = models.TextField()

    # Uma Receita pode ter MÚLTIPLAS Categorias, e uma Categoria pode ter MÚLTIPLAS Receitas.
    categoria = models.ManyToManyField(
        Categoria, 
        related_name='receitas'
    )

    def __str__(self):
        return self.titulo