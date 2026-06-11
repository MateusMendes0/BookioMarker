from django.urls import path
from apps.leitura.views import adicionar_leitura_view, registrar_sessao_view

urlpatterns = [
    path('leitura/adicionar/', adicionar_leitura_view, name='adicionar_leitura'),
    path('leitura/registrar-sessao/', registrar_sessao_view, name='registrar_sessao'),
]
