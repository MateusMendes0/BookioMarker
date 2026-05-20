from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.leitura.models import Leitura, SessaoLeitura

class SessaoLeituraInline(TabularInline):
    model = SessaoLeitura
    extra = 1
    readonly_fields = ('data_leitura',)

@admin.register(Leitura)
class LeituraAdmin(ModelAdmin):
    list_display = ('pessoa', 'livro', 'status', 'progresso_visual')
    list_filter = ('status', 'pessoa')
    search_fields = ('livro__titulo', 'pessoa__username')
    inlines = [SessaoLeituraInline]
    
    def progresso_visual(self, obj):
        if obj.livro.total_paginas > 0:
            porcentagem = (obj.paginas_lidas / obj.livro.total_paginas) * 100
            return f"{obj.paginas_lidas}/{obj.livro.total_paginas} ({porcentagem:.1f}%)"
        return "0%"
    progresso_visual.short_description = "Progresso"

@admin.register(SessaoLeitura)
class SessaoLeituraAdmin(ModelAdmin):
    list_display = ('leitura', 'data_leitura', 'paginas_avancadas')
    list_filter = ('data_leitura',)