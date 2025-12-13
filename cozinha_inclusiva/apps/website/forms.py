from django import forms
from apps.comentarios.models import Comentario


class BuscaForm(forms.Form):
    termo = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Buscar receita, ingrediente ou categoria...',
        })
    )


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva seu comentário aqui...',
                'rows': 3,
            })
        }
        labels = {
            'texto': ''
        }
