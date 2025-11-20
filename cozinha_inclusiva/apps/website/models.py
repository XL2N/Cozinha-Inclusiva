from django.db import models

class ConfiguracaoWebsite(models.Model):
    # Informações Básicas
    titulo_site = models.CharField(
        max_length=255, 
        default="Cozinha Inclusiva",
        verbose_name="Título Principal do Site"
    )
    descricao_meta = models.CharField(
        max_length=500,
        verbose_name="Descrição para Motores de Busca (SEO)"
    )
    email_contato = models.EmailField(
        verbose_name="E-mail de Contato Principal"
    )
    telefone_contato = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Telefone (WhatsApp)"
    )
    
    # Redes Sociais
    link_instagram = models.URLField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Link para Instagram"
    )
    link_facebook = models.URLField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Link para Facebook"
    )

    # Logo e Favicon
    logo_header = models.ImageField(
        upload_to='site/', 
        blank=True, 
        null=True,
        verbose_name="Logo do Cabeçalho"
    )
    
    class Meta:
        verbose_name = "Configuração do Website"
        verbose_name_plural = "Configurações do Website"
    
    def __str__(self):
        return self.titulo_site

    # MÉTODO PARA GARANTIR APENAS UMA LINHA
    def save(self, *args, **kwargs):
        # Se um registro já existe, atualiza ele em vez de criar um novo.
        if ConfiguracaoWebsite.objects.exists() and not self.pk:
            instance = ConfiguracaoWebsite.objects.get()
            self.pk = instance.pk
        super(ConfiguracaoWebsite, self).save(*args, **kwargs)