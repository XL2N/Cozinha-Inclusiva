from django.db import models
from apps.receitas.models import Receita
from apps.administrativo.models import Usuario 

class Comentario(models.Model):

    # Relacionamento N:1 (Um Comentário RECEBE UMA Receita)
    receita = models.ForeignKey(
        Receita, 
        on_delete=models.CASCADE, 
        related_name='comentarios', 
        verbose_name="Receita"
    )

    # Relacionamento N:1 (Um Comentário É FEITO por UM Usuário)
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='comentarios_feitos', 
        verbose_name="Usuário"
    )

    texto = models.TextField(verbose_name="Comentário")
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-data_hora']

    def __str__(self):
        return f"Comentário em {self.receita.titulo} por {self.usuario.username if self.usuario else 'Usuário Deletado'}"


class PalavraBloqueada(models.Model):
    palavra = models.CharField(max_length=100, unique=True, verbose_name="Palavra/Termo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Palavra Bloqueada"
        verbose_name_plural = "Palavras Bloqueadas"
        ordering = ['palavra']

    def __str__(self):
        return self.palavra