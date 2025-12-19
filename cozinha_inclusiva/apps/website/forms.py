from django import forms
from apps.comentarios.models import Comentario



class BuscaForm(forms.Form):
    termo = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Buscar receita, ingrediente ou categoria...'
        })
    )
    sem_lactose = forms.BooleanField(required=False, label='Sem Lactose')
    sem_gluten = forms.BooleanField(required=False, label='Sem Glúten')
    vegano = forms.BooleanField(required=False, label='Vegano')
    vegetariano = forms.BooleanField(required=False, label='Vegetariano')


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
