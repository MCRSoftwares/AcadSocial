# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v006a

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
from contas import errors, methods
from universidades.models import UniversidadeModel, CursoModel
from contas import constants

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

    first_name_attrs = {'placeholder': 'Nome', 'class': 'form-control'}
    last_name_attrs = {'placeholder': 'Sobrenome', 'class': 'form-control'}
    email_attrs = {'placeholder': 'E-mail', 'class': 'form-control'}
    password_attrs = {'placeholder': 'Senha', 'class': 'form-control'}
    password_conf_attrs = {'placeholder': 'Confirme a senha', 'class': 'form-control'}

    # Criação dos emails disponíveis para cadastro

    email_list = {(emails, emails) for emails in constants.VALID_EMAILS}

    # Criação dos campos

    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs=first_name_attrs), label='nome')
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs=last_name_attrs), label='sobrenome')
    email_front = forms.CharField(max_length=128, widget=forms.TextInput(attrs=email_attrs), label='e-mail')
    email_back = forms.ChoiceField(choices=email_list, widget=forms.Select(attrs=email_attrs))
    email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs=password_attrs), label='senha')
    password_conf = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs=password_conf_attrs),
                                    label='confirmar senha')

    def clean(self):

        nome = self.cleaned_data.get('first_name')
        sobrenome = self.cleaned_data.get('last_name')

        if nome and len(nome) < 2:
            raise forms.ValidationError(errors.erro_cadastro['nome_incompleto'], code='cadastro_e05')

        if sobrenome and len(sobrenome) < 2:
            raise forms.ValidationError(errors.erro_cadastro['sobrenome_incompleto'], code='cadastro_e06')

        # Checa se os campos password e password_conf estão corretos (iguais).

        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')

        if methods.validar_senhas(password, password_conf) == 'invalida':
            raise forms.ValidationError(errors.erro_cadastro['senha_invalida'], code='cadastro_e04')

        if methods.validar_senhas(password, password_conf) == 'diferentes':
            raise forms.ValidationError(errors.erro_cadastro['senhas_diferentes'], code='cadastro_e01')

        return self.cleaned_data

    def clean_email(self):

        try:
            email_front = self.cleaned_data['email_front']
        except:
            raise forms.ValidationError(errors.erro_cadastro['email_invalido'], code='cadastro_e02')

        email_back = self.cleaned_data['email_back']

        email = email_front + email_back

        # Checa se o e-mail já existe.

        try:
            UsuarioModel.object.get(email=email)

        except UsuarioModel.DoesNotExist:
            return email

        raise forms.ValidationError(errors.erro_cadastro['email_ja_existente'], code='cadastro_e03')

    class Meta:
        model = UsuarioModel
        fields = ('first_name', 'last_name', 'email_front', 'email_back', 'password', 'password_conf')


class PerfilCadastroForm(forms.ModelForm):

    # Criação dos atributos dos campos

    universidade_attrs = {'placeholder': 'Universidade', 'class': 'form-control'}
    curso_attrs = {'placeholder': 'Curso', 'class': 'form-control'}
    foto_attrs = {'class': 'form-control'}
    data_nascimento_attrs = {'class': 'form-control'}

    # Criação das listas de dia, mês e ano

    dia_list = [(x, str(x)) for x in range(1, 32)]
    dia_list.insert(0, (0, 'Dia'))

    mes_list = [(x, str(x)) for x in range(1, 13)]
    mes_list.insert(0, (0, 'Mês'))

    ano_list = [(x, str(x)) for x in range(datetime.today().year - 100, datetime.today().year + 1)]
    ano_list.insert(0, (0, 'Ano'))

    # Criação dos campos

    dia = forms.ChoiceField(choices=dia_list, widget=forms.Select(data_nascimento_attrs))
    mes = forms.ChoiceField(choices=mes_list, widget=forms.Select(data_nascimento_attrs))
    ano = forms.ChoiceField(choices=ano_list, widget=forms.Select(data_nascimento_attrs))

    universidade = forms.ModelChoiceField(queryset=UniversidadeModel.objects, empty_label='Universidade',
                                          label='universidade', widget=forms.Select(attrs=universidade_attrs))
    curso = forms.ModelChoiceField(queryset=CursoModel.objects, empty_label='Curso', label='curso',
                                   widget=forms.Select(attrs=curso_attrs))
    foto = forms.ImageField(widget=forms.FileInput(attrs=foto_attrs), required=False, label='foto')

    def clean(self):

        # Checa se a data de nascimento é válida

        dia_nasc = self.cleaned_data.get('dia')
        mes_nasc = self.cleaned_data.get('mes')
        ano_nasc = self.cleaned_data.get('ano')

        nasc_str = str(dia_nasc) + '-' + str(mes_nasc) + '-' + str(ano_nasc)

        try:
            datetime.strptime(nasc_str, '%d-%m-%Y')
        except ValueError:
            raise forms.ValidationError(errors.erro_cadastro['data_incorreta'], code='cadastro_e04')

    class Meta:
        model = PerfilModel
        fields = ('dia', 'mes', 'ano', 'universidade', 'curso', 'foto')


class UsuarioLoginForm(forms.ModelForm):

    # Criação dos atributos dos campos

    email_attrs = {'placeholder': 'E-mail', 'class': 'form-control'}
    password_attrs = {'placeholder': 'Senha', 'class': 'form-control'}

    # Criação dos campos

    email = forms.EmailField(max_length=128, widget=forms.EmailInput(attrs=email_attrs), label='e-mail')
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs=password_attrs), label='senha')

    def __init__(self, request=None, *args, **kwargs):
        super(UsuarioLoginForm, self).__init__(*args, **kwargs)
        self.request = request
        self.usuario = None

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


class EnviarTokenForm(forms.ModelForm):

    # Criação dos atributos do campo

    email_attrs = {'placeholder': 'E-mail', 'class': 'form-control'}

    # Criação do campo

    email = forms.EmailField(max_length=128, widget=forms.EmailInput(attrs=email_attrs), label='e-mail')

    def clean_email(self):

        email = self.cleaned_data['email']

        # Checa se o e-mail existe.

        try:
            UsuarioModel.object.get(email=email)

            return email
        except UsuarioModel.DoesNotExist:
            raise forms.ValidationError(errors.erro_enviar_token['email_invalido'], code='enviar_token_e01')

    def clean(self):
        email = self.cleaned_data.get('email')

        # Checa se o e-mail existe.

        # Método clean(self) alterado para que ele aceite o valor do email, caso contrário,
        # ele tentará registrar um novo usuário com este email.

        try:
            UsuarioModel.object.get(email=email)
        except UsuarioModel.DoesNotExist:
            return self.cleaned_data

        return self.cleaned_data

    class Meta:
        model = UsuarioModel
        fields = ('email',)


class SenhaResetForm(forms.ModelForm):

    # Criação dos atributos dos campos

    senha_attrs = {'placeholder': 'Senha', 'class': 'form-control'}
    senha_conf_attrs = {'placeholder': 'Confirme a senha', 'class': 'form-control'}

    # Criação dos campos

    senha = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs=senha_attrs), label='senha',
                            required=True)
    senha_conf = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs=senha_conf_attrs),
                                 label='confirme a senha', required=True)

    def clean(self):
        senha = self.cleaned_data.get('senha')
        senha_conf = self.cleaned_data.get('senha_conf')

        if methods.validar_senhas(senha, senha_conf) == 'deferente':
            raise forms.ValidationError(errors.erro_enviar_token['senhas_diferentes'], code='enviar_token_e02')

        elif methods.validar_senhas(senha, senha_conf) == 'invalida':
            raise forms.ValidationError(errors.erro_enviar_token['senha_invalida'], code='enviar_token_e03')

        return self.cleaned_data

    class Meta:
        model = UsuarioModel
        fields = ('senha', 'senha_conf')