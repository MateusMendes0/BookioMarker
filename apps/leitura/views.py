from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.catalogo.models import Livro
from apps.leitura.models import Leitura, SessaoLeitura

@login_required(login_url='login')
@require_POST
def adicionar_leitura_view(request):
    livro_id = request.POST.get('livro_id')
    status = request.POST.get('status')
    
    livro = get_object_or_404(Livro, id=livro_id)
    
    leitura, created = Leitura.objects.get_or_create(
        pessoa=request.user,
        livro=livro
    )
    
    leitura.status = status
    if status == 'LIDO':
        leitura.paginas_lidas = livro.total_paginas
    elif status == 'QUERO_LER':
        leitura.paginas_lidas = 0
        
    leitura.save()
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('dashboard')

@login_required(login_url='login')
@require_POST
def registrar_sessao_view(request):
    leitura_id = request.POST.get('leitura_id')
    try:
        paginas_avancadas = int(request.POST.get('paginas_avancadas', 0))
    except ValueError:
        paginas_avancadas = 0
        
    leitura = get_object_or_404(Leitura, id=leitura_id, pessoa=request.user)
    
    if paginas_avancadas > 0:
        paginas_restantes = leitura.livro.total_paginas - leitura.paginas_lidas
        if paginas_avancadas > paginas_restantes:
            paginas_avancadas = paginas_restantes
            
        if paginas_avancadas > 0:
            SessaoLeitura.objects.create(
                leitura=leitura,
                paginas_avancadas=paginas_avancadas
            )
            
    return redirect('dashboard')

