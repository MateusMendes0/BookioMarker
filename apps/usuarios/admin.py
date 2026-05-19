from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import Usuario, MetaAnual

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin, ModelAdmin):
    # Adicionando os campos personalizados aos fieldsets padrão do UserAdmin
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            'Informações Adicionais',
            {
                'fields': (
                    'nickname',
                    'nome',
                    'data_nascimento',
                    'genero',
                    'pais',
                    'bio',
                    'streak_atual',
                    'maior_streak',
                    'total_livros_lidos',
                    'total_paginas_lidas',
                    'ultima_data_lida',
                )
            },
        ),
    )
    list_display = ('username', 'email', 'nome', 'nickname', 'is_staff')
    search_fields = ('username', 'email', 'nome', 'nickname')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'genero')

@admin.register(MetaAnual)
class MetaAnualAdmin(ModelAdmin):
    list_display = ('usuario', 'ano', 'quantidade_alvo')
    list_filter = ('ano',)
    search_fields = ('usuario__username', 'usuario__nome')
