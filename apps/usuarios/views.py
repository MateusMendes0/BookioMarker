from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from apps.usuarios.forms import CadastroForm, LoginForm
from apps.leitura.models import Leitura

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = CadastroForm()
        
    return render(request, 'usuarios/cadastro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    usuario = request.user
    
    leituras_lendo = Leitura.objects.filter(pessoa=usuario, status='LENDO').select_related('livro')
    leituras_lidas = Leitura.objects.filter(pessoa=usuario, status='LIDO').select_related('livro')
    leituras_quero_ler = Leitura.objects.filter(pessoa=usuario, status='QUERO_LER').select_related('livro')
    
    context = {
        'usuario': usuario,
        'leituras_lendo': leituras_lendo,
        'leituras_lidas': leituras_lidas,
        'leituras_quero_ler': leituras_quero_ler,
    }
    return render(request, 'usuarios/dashboard.html', context)

