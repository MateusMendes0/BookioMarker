from django.db import models
from django_countries.fields import CountryField
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Idioma(models.TextChoices):
    PORTUGUES = 'pt', 'Português'
    INGLES = 'en', 'Inglês'
    ESPANHOL = 'es', 'Espanhol'
    FRANCES = 'fr', 'Francês'
    ALEMAO = 'de', 'Alemão'
    
    class Meta:
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"

class Autor(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografia")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    country = CountryField(
        blank=True,
        null=True,
        verbose_name="País",
    )


    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nome']

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome") 
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

class Livro(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True, verbose_name="ISBN")
    total_paginas = models.PositiveIntegerField(verbose_name="Total de Páginas")
    capa_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Capa")
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros', verbose_name="Autor")
    categorias = models.ManyToManyField(Categoria, related_name='livros', verbose_name="Categorias")
    data_publicacao = models.DateField(blank=True, null=True, verbose_name="Data de Publicação")
    capa = models.ImageField(
        upload_to="livros/capas/",
        blank=True,
        null=True,
    )
    idioma = models.CharField(
        max_length=2,
        choices=Idioma.choices,
        default=Idioma.PORTUGUES,
        verbose_name="Idioma",
    )

    def __str__(self):
        return f"{self.titulo} - {self.autor.nome}"
    
    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"


class Avaliacao(models.Model):
    pessoa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avaliacoes')
    livro = models.ForeignKey('catalogo.Livro', on_delete=models.CASCADE, related_name='avaliacoes')
    
    nota = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    texto_resenha = models.TextField(blank=True, null=True)
    
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.pessoa.username} para {self.livro.titulo} - Nota: {self.nota}"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ['pessoa', 'livro']