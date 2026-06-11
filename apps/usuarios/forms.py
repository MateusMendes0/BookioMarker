from django import forms
from apps.usuarios.models import Usuario

class CadastroForm(forms.Form):
    nome = forms.CharField(
        max_length=150,
        required=True,
        label="Nome completo",
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'})
    )
    nickname = forms.CharField(
        max_length=150,
        required=True,
        label="Nickname",
        widget=forms.TextInput(attrs={'placeholder': 'Escolha um apelido'})
    )
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'})
    )
    senha = forms.CharField(
        required=True,
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'})
    )
    confirmar_senha = forms.CharField(
        required=True,
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Usuario.objects.filter(username=nickname).exists() or Usuario.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("Este nickname já está em uso.")
        return nickname

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        usuario = Usuario.objects.create_user(
            username=cleaned_data.get('nickname'),
            email=cleaned_data.get('email'),
            password=cleaned_data.get('senha'),
            nome=cleaned_data.get('nome'),
            nickname=cleaned_data.get('nickname')
        )
        return usuario


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'})
    )
    senha = forms.CharField(
        required=True,
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')

        if email and senha:
            try:
                usuario = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                raise forms.ValidationError("Usuário com este e-mail não existe.")

            from django.contrib.auth import authenticate
            user = authenticate(username=usuario.username, password=senha)
            if user is None:
                raise forms.ValidationError("E-mail ou senha incorretos.")
            
            cleaned_data['user'] = user

        return cleaned_data
