from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class Leitura(models.Model):
    STATUS_CHOICES = [
        ('QUERO_LER', 'Quero Ler'),
        ('LENDO', 'Lendo'),
        ('LIDO', 'Lido'),
        ('ABANDONADO', 'Abandonado'),
    ]

    pessoa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leituras')
    livro = models.ForeignKey('catalogo.Livro', on_delete=models.CASCADE, related_name='leituras_usuarios')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='QUERO_LER')
    paginas_lidas = models.PositiveIntegerField(default=0)
    
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    
    nota = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.pessoa.username} - {self.livro.titulo} ({self.get_status_display()})"

    def clean(self):
        if self.livro and self.paginas_lidas > self.livro.total_paginas:
            raise ValidationError({'paginas_lidas': f"Não pode ser maior que o total de páginas do livro ({self.livro.total_paginas})."})

    class Meta:
        verbose_name = "Leitura"
        verbose_name_plural = "Leituras"
        unique_together = ['pessoa', 'livro']


class SessaoLeitura(models.Model):
    leitura = models.ForeignKey(Leitura, on_delete=models.CASCADE, related_name='sessoes')
    data_leitura = models.DateField(auto_now_add=True)
    paginas_avancadas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.leitura.livro.titulo} - {self.paginas_avancadas} págs em {self.data_leitura}"

    class Meta:
        verbose_name = "Sessão de Leitura"
        verbose_name_plural = "Sessões de Leitura"

@receiver(post_save, sender=SessaoLeitura)
def atualizar_progresso_leitura(sender, instance, created, **kwargs):
    if created:
        leitura = instance.leitura
        
        leitura.paginas_lidas += instance.paginas_avancadas
        
        if leitura.paginas_lidas >= leitura.livro.total_paginas:
            leitura.paginas_lidas = leitura.livro.total_paginas
            leitura.status = 'LIDO'
            
        elif leitura.status == 'QUERO_LER' and leitura.paginas_lidas > 0:
            leitura.status = 'LENDO'
            
        leitura.save()