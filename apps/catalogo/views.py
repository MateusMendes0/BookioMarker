from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.catalogo.models import Livro
from apps.leitura.models import Leitura

@login_required(login_url='login')
def livros_lista_view(request):
    livros = Livro.objects.all().select_related('autor')
    
    # Mapeia as leituras do usuário logado
    leituras_usuario = Leitura.objects.filter(pessoa=request.user)
    leitura_status_map = {leitura.livro_id: leitura.status for leitura in leituras_usuario}
    
    # Atribui o status correspondente para cada livro
    for livro in livros:
        livro.status_leitura = leitura_status_map.get(livro.id)
        
    return render(request, 'catalogo/livros_lista.html', {'livros': livros})

