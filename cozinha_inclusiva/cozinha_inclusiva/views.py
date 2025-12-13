from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CadastroForm

### LOGIN ### 
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_adm')
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
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('home_adm')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})