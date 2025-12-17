from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import LoginForm, CadastroForm

### LOGIN ### 
def login_user(request):
    # Redireciona usuários autenticados
    if request.user.is_authenticated:
        if request.user.tipo_usuario in ['ADMIN', 'AUTOR']:
            return redirect('home_adm')
        else:
            return redirect('inicio')
    
    # Caminho feliz do login
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # se o usuario for admin ou autor, redireciona para a tela home_adm
                if user.tipo_usuario in ['ADMIN', 'AUTOR']:
                    return redirect('home_adm')
                else:
                    return redirect('inicio')

        messages.error(request, "Usuário ou senha inválidos")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

### LOGOUT ###
def logout_user(request):
    logout(request)
    return redirect('inicio')

### CADASTRO ###
def cadastro_user(request):
    # Redireciona usuários autenticados
    if request.user.is_authenticated:
        if request.user.tipo_usuario in ['ADMIN', 'AUTOR']:
            return redirect('home_adm')
        else:
            return redirect('inicio')
    
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.tipo_usuario = 'LEITOR'  # Define o tipo como LEITOR
                user.save()
                
                # Adiciona o usuário ao grupo "Leitor"
                leitor_group, created = Group.objects.get_or_create(name='Leitor')
                user.groups.add(leitor_group)
                
                login(request, user)
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect('inicio')  # Redireciona para início, não home_adm
            except Exception as e:
                messages.error(request, f"Erro ao criar conta: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})