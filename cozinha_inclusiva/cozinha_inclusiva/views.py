from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from apps.administrativo.models import Usuario

from .forms import CadastroForm, LoginForm


def _login_mock_user(request, username='admin_mock', tipo_usuario='ADMIN'):
    username = (username or 'admin_mock').strip() or 'admin_mock'
    user, created = Usuario.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@mock.local',
            'first_name': 'Usuario',
            'last_name': 'Mock',
            'tipo_usuario': tipo_usuario,
            'is_staff': tipo_usuario == 'ADMIN',
        },
    )

    changed = False
    if created:
        user.set_unusable_password()
        changed = True
    if user.tipo_usuario != tipo_usuario:
        user.tipo_usuario = tipo_usuario
        changed = True
    if tipo_usuario == 'ADMIN' and not user.is_staff:
        user.is_staff = True
        changed = True
    if changed:
        user.save()

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return user


def login_user(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'tipo_usuario', 'LEITOR') in ['ADMIN', 'AUTOR']:
            return redirect('home_adm')
        return redirect('inicio')

    if request.method == 'POST':
        if settings.MOCK_AUTH:
            user = _login_mock_user(
                request,
                username=request.POST.get('username') or 'admin_mock',
                tipo_usuario='ADMIN',
            )
            messages.success(request, f'Login mockado ativo para {user.username}.')
            return redirect('home_adm')

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if getattr(user, 'tipo_usuario', 'LEITOR') in ['ADMIN', 'AUTOR']:
                    return redirect('home_adm')
                return redirect('inicio')

        messages.error(request, 'Usuario ou senha invalidos')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('inicio')


def cadastro_user(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'tipo_usuario', 'LEITOR') in ['ADMIN', 'AUTOR']:
            return redirect('home_adm')
        return redirect('inicio')

    if request.method == 'POST':
        if settings.MOCK_AUTH:
            user = _login_mock_user(
                request,
                username=request.POST.get('username') or 'leitor_mock',
                tipo_usuario='LEITOR',
            )
            messages.success(request, f'Cadastro mockado ativo para {user.username}.')
            return redirect('inicio')

        form = CadastroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.tipo_usuario = 'LEITOR'
                user.save()

                leitor_group, created = Group.objects.get_or_create(name='Leitor')
                user.groups.add(leitor_group)

                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('inicio')
            except Exception as e:
                messages.error(request, f'Erro ao criar conta: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulario.')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})
