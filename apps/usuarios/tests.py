from django.test import TestCase
from django.urls import reverse
from apps.usuarios.models import Usuario

class AuthenticationTests(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.cadastro_url = reverse('cadastro')
        self.dashboard_url = reverse('dashboard')
        self.root_url = '/'

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.root_url)
        self.assertRedirects(response, self.login_url)

        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")

    def test_user_registration_success(self):
        data = {
            'nome': 'João Silva',
            'nickname': 'joaosilva',
            'email': 'joao@email.com',
            'senha': 'senha123password',
            'confirmar_senha': 'senha123password'
        }
        response = self.client.post(self.cadastro_url, data)
        self.assertRedirects(response, self.dashboard_url)

        self.assertTrue(Usuario.objects.filter(email='joao@email.com').exists())

        usuario = Usuario.objects.get(email='joao@email.com')
        self.assertEqual(int(self.client.session['_auth_user_id']), usuario.pk)

    def test_user_registration_password_mismatch(self):
        data = {
            'nome': 'João Silva',
            'nickname': 'joaosilva',
            'email': 'joao@email.com',
            'senha': 'senha123password',
            'confirmar_senha': 'diferente123'
        }
        response = self.client.post(self.cadastro_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], None, "As senhas não coincidem.")

    def test_user_login_success(self):
        usuario = Usuario.objects.create_user(
            username='usertest',
            email='test@email.com',
            password='mysecretpassword',
            nome='Test User',
            nickname='usertest'
        )

        data = {
            'email': 'test@email.com',
            'senha': 'mysecretpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, self.dashboard_url)

        self.assertEqual(int(self.client.session['_auth_user_id']), usuario.pk)

    def test_user_login_invalid_credentials(self):
        data = {
            'email': 'inexistente@email.com',
            'senha': 'senha'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], None, "Usuário com este e-mail não existe.")

