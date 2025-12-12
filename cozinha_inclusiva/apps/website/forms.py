from django import forms


class BuscaForm(forms.Form):
    termo = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Buscar receita, ingrediente ou categoria...',
        })
    )
