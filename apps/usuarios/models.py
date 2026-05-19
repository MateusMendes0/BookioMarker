from django.utils import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class Usuario(AbstractUser):
    class Genero(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMININO = 'F', 'Feminino'

    nickname = models.CharField(max_length=150, unique=True, verbose_name="Nickname")
    nome = models.CharField(max_length=150, verbose_name="Nome")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    genero = models.CharField(
        max_length=1,
        choices=Genero.choices,
        verbose_name="Gênero",
        null=True,
        blank=True,
    )

    pais = CountryField(
        verbose_name="País",
        blank=True,
        null=True,
    )

    bio = models.CharField(max_length=150, verbose_name="Bio")

    streak_atual = models.PositiveIntegerField(default=0)
    maior_streak = models.PositiveIntegerField(default=0)
    total_livros_lidos = models.PositiveIntegerField(default=0)
    total_paginas_lidas= models.PositiveIntegerField(default=0)
    
    ultima_data_lida = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class MetaAnual(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='metas_anuais')
    ano = models.PositiveIntegerField()
    quantidade_alvo = models.PositiveIntegerField(default=12)

    def __str__(self):
        return f"Meta {self.ano} - {self.usuario.username}"
    
    class Meta:
        unique_together = ['usuario', 'ano']