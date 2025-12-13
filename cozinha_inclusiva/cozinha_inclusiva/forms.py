from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from apps.administrativo.models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg mb-2',
        'placeholder': 'Usuário'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg mb-2',
        'placeholder': 'Senha'})
    )

class CadastroForm(UserCreationForm):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Digite seu nome de usuário",
            "autocomplete": "username"
        }),
        help_text="Requerido. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.",
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Digite sua senha",
            "autocomplete": "new-password"
        }),
        help_text="Sua senha deve conter pelo menos 8 caracteres.",
    )

    password2 = forms.CharField(
        label="Confirmação de Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Confirme sua senha",
            "autocomplete": "new-password"
        }),
        help_text="Digite a mesma senha para verificação.",
    )

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2']