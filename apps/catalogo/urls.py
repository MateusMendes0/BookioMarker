from django.urls import path
from apps.catalogo.views import livros_lista_view

urlpatterns = [
    path('livros/', livros_lista_view, name='livros_lista'),
]
