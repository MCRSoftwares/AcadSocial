# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v005a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição dos formulários relacionados à aplicação de contas (cadastro/login).
"""

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from contas.models import UsuarioModel, PerfilModel
from django.contrib.auth import authenticate
from django import forms
from datetime import datetime
from contas import errors
from universidades.models import UniversidadeModel, CursoModel

# Forms relacionados à página do admin


class UsuarioCreationForm(UserCreationForm):

    def __init__(self, *args, **kargs):
        super(UsuarioCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = UsuarioModel
        fields = ('email',)


class UsuarioChangeForm(UserChangeForm):

    def __init__(self, *args, **kargs):
        super(UsuarioChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = UsuarioModel
        fields = ()


# Forms relacionados à contas/views


class UsuarioCadastroForm(forms.ModelForm):

    # Criação dos atributos dos campos

    first_name_attrs = {'placeholder': 'Nome'}
    last_name_attrs = {'placeholder': 'Sobrenome'}
    email_attrs = {'placeholder': 'E-mail'}
    password_attrs = {'placeholder': 'Senha'}
    password_conf_attrs = {'placeholder': 'Confirme a senha'}

    # Criação dos campos

    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs=first_name_attrs))
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs=last_name_attrs))
    email = forms.EmailField(max_length=128, widget=forms.TextInput(attrs=email_attrs))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs=password_attrs))
    password_conf = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs=password_conf_attrs))

    def clean(self):

        # Checa se os campos password e password_conf estão corretos (iguais).

        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')

        if password != password_conf:
            raise forms.ValidationError(errors.erro_cadastro['senhas_diferentes'], code='cadastro_e01')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']

        # Checa se o e-mail já existe.

        try:
            UsuarioModel.object.get(email=email)

        except UsuarioModel.DoesNotExist:
            return email

        raise forms.ValidationError(errors.erro_cadastro['email_ja_existente'], code='cadastro_e02')

    class Meta:
        model = UsuarioModel
        fields = ('first_name', 'last_name', 'email', 'password', 'password_conf')


class PerfilCadastroForm(forms.ModelForm):

    # Criação dos atributos dos campos

    universidade_attrs = {'placeholder': 'Universidade'}
    campus_attrs = {'placeholder': 'Campus'}
    curso_attrs = {'placeholder': 'Curso'}
    foto_attrs = {}

    # Criação das listas de dia, mês e ano

    dia_list = [(x, str(x)) for x in range(1, 32)]
    dia_list.insert(0, (0, 'Dia'))

    mes_list = [(x, str(x)) for x in range(1, 13)]
    mes_list.insert(0, (0, 'Mês'))

    ano_list = [(x, str(x)) for x in range(datetime.today().year - 100, datetime.today().year + 1)]
    ano_list.insert(0, (0, 'Ano'))

    # Criação dos campos

    dia = forms.ChoiceField(choices=dia_list)
    mes = forms.ChoiceField(choices=mes_list)
    ano = forms.ChoiceField(choices=ano_list)

    universidade = forms.ModelChoiceField(queryset=UniversidadeModel.objects, empty_label='Universidade')
    curso = forms.ModelChoiceField(queryset=CursoModel.objects, empty_label='Curso')
    foto = forms.ImageField(widget=forms.FileInput(attrs=foto_attrs))

    def clean(self):

        # Checa se a data de nascimento é válida

        dia_nasc = self.cleaned_data.get('dia')
        mes_nasc = self.cleaned_data.get('mes')
        ano_nasc = self.cleaned_data.get('ano')

        nasc_str = str(dia_nasc) + '-' + str(mes_nasc) + '-' + str(ano_nasc)

        try:
            datetime.strptime(nasc_str, '%d-%m-%Y')
        except ValueError:
            raise forms.ValidationError(errors.erro_cadastro['senhas_diferentes'], code='cadastro_e03')

    class Meta:
        model = PerfilModel
        fields = ('dia', 'mes', 'ano', 'universidade', 'curso', 'foto')


class UsuarioLoginForm(forms.ModelForm):

    # Criação dos atributos dos campos

    email_attrs = {'placeholder': 'E-mail'}
    password_attrs = {'placeholder': 'Senha'}

    # Criação dos campos

    email = forms.EmailField(max_length=128, widget=forms.EmailInput(attrs=email_attrs))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs=password_attrs))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.usuario = None
        super(UsuarioLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.usuario = authenticate(username=email, password=password)

            if not self.usuario:
                # Se o usuário for nulo, então o email ou a senha estão incorretos.

                raise forms.ValidationError(errors.erro_login['login_invalido'], code='login_e01')

            elif not self.usuario.is_active:
                # Caso o login esteja correto, mas o usuário não esteja ativado (conta cancelada / conta não confirmada)

                raise forms.ValidationError(errors.erro_login['email_inativo'], code='login_e02')

        return self.cleaned_data

    def get_usuario(self):
        return self.usuario

    class Meta:
        model = UsuarioModel
        fields = ('email', 'password',)
