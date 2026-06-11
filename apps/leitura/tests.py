from django.test import TestCase
from django.urls import reverse
from apps.usuarios.models import Usuario
from apps.catalogo.models import Autor, Livro
from apps.leitura.models import Leitura, SessaoLeitura

class LeituraTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='leitor',
            email='leitor@email.com',
            password='senha',
            nome='Leitor Teste',
            nickname='leitor'
        )
        
        self.autor = Autor.objects.create(nome='Machado de Assis')
        self.livro = Livro.objects.create(
            titulo='Dom Casmurro',
            total_paginas=200,
            autor=self.autor
        )
        
        self.client.login(username='leitor', password='senha')

    def test_adicionar_leitura_nova(self):
        url = reverse('adicionar_leitura')
        data = {
            'livro_id': self.livro.id,
            'status': 'QUERO_LER'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(Leitura.objects.filter(pessoa=self.user, livro=self.livro, status='QUERO_LER').exists())

    def test_atualizar_leitura_existente(self):
        leitura = Leitura.objects.create(
            pessoa=self.user,
            livro=self.livro,
            status='QUERO_LER'
        )
        
        url = reverse('adicionar_leitura')
        data = {
            'livro_id': self.livro.id,
            'status': 'LENDO'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        leitura.refresh_from_db()
        self.assertEqual(leitura.status, 'LENDO')

    def test_registrar_sessao_leitura_atualiza_paginas_e_status(self):
        leitura = Leitura.objects.create(
            pessoa=self.user,
            livro=self.livro,
            status='LENDO',
            paginas_lidas=10
        )
        
        url = reverse('registrar_sessao')
        data = {
            'leitura_id': leitura.id,
            'paginas_avancadas': 20
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        leitura.refresh_from_db()
        self.assertEqual(leitura.paginas_lidas, 30)
        self.assertEqual(leitura.status, 'LENDO')

    def test_registrar_sessao_leitura_excede_limite_cap(self):
        leitura = Leitura.objects.create(
            pessoa=self.user,
            livro=self.livro,
            status='LENDO',
            paginas_lidas=190
        )
        
        url = reverse('registrar_sessao')
        data = {
            'leitura_id': leitura.id,
            'paginas_avancadas': 50
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        leitura.refresh_from_db()
        self.assertEqual(leitura.paginas_lidas, 200)
        self.assertEqual(leitura.status, 'LIDO')

