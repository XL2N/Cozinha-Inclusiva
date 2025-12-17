from django.contrib.auth.models import AbstractUser
from django.db import models

# MODEL USUARIO
class Usuario(AbstractUser):

    TIPO_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('LEITOR', 'Leitor'),
        ('AUTOR', 'Autor'),
    ]

    # Redefine o campo 'groups' com um related_name único
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set', 
        related_query_name='usuario',
    )

    # Redefine o campo 'user_permissions' com um related_name único
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_permissions_set', 
        related_query_name='usuario_permission',
    )

    tipo_usuario = models.CharField(
        max_length=10, 
        choices=TIPO_CHOICES, 
        default='LEITOR', 
        verbose_name="Tipo"
    )

    imagem = models.ImageField(
        upload_to='usuarios/fotos/', 
        blank=True, 
        null=True, 
        verbose_name="Imagem"
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username
    
# MODEL DESTAQUE CARROUSSEL
