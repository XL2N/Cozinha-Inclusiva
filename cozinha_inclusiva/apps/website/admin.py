from django.contrib import admin
from .models import ConfiguracaoWebsite

@admin.register(ConfiguracaoWebsite)
class ConfiguracaoWebsiteAdmin(admin.ModelAdmin):

    # Oculta a lista e o botão "Adicionar" na visualização da lista, 
    def has_add_permission(self, request):
        return not ConfiguracaoWebsite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False # Não permite deletar a única linha
    
    list_display = ('titulo_site', 'email_contato')