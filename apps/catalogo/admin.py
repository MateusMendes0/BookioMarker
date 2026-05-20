from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Autor, Categoria, Livro, Avaliacao

@admin.register(Autor)
class AutorAdmin(ModelAdmin):
    list_display = ('nome', 'country', 'data_nascimento')
    search_fields = ('nome',)
    list_filter = ('country',)

@admin.register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Livro)
class LivroAdmin(ModelAdmin):
    list_display = ('titulo', 'autor', 'idioma', 'total_paginas', 'data_publicacao')
    search_fields = ('titulo', 'isbn', 'autor__nome')
    list_filter = ('idioma', 'categorias', 'data_publicacao')
    autocomplete_fields = ('autor',)
    filter_horizontal = ('categorias',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(ModelAdmin):
    list_display = ('pessoa', 'livro', 'nota', 'data_avaliacao')
    list_filter = ('nota', 'data_avaliacao')
    search_fields = ('pessoa__username', 'livro__titulo', 'texto_resenha')