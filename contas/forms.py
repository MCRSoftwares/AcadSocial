# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v008a

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
from contas.methods import validar_senhas, validar_palavra
from contas.errors import erro_cadastro, erro_enviar_token, erro_login
from universidades.models import UniversidadeModel, CursoModel
from contas.constants import VALID_EMAILS

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

    first_name_attrs = {'placeholder': 'Nome', 'class': 'form-control', 'id': 'nomeID'}
    last_name_attrs = {'placeholder': 'Sobrenome', 'class': 'form-control', 'id': 'sobrenomeID'}
    email_attrs = {'placeholder': 'E-mail', 'class': 'form-control', 'id': 'emailID'}
    password_attrs = {'placeholder': 'Senha', 'class': 'form-control'}
    password_conf_attrs = {'placeholder': 'Confirme a senha', 'class': 'form-control'}

    # Criação dos emails disponíveis para cadastro

    email_list = {(emails, emails) for emails in VALID_EMAILS}

    # Criação dos campos

    first_name = forms.CharField(min_length=2, max_length=128, widget=forms.TextInput(attrs=first_name_attrs))
    last_name = forms.CharField(min_length=2, max_length=128, widget=forms.TextInput(attrs=last_name_attrs),
                                label='sobrenome')
    email_front = forms.CharField(min_length=2, max_length=128, widget=forms.TextInput(attrs=email_attrs),
                                  label='e-mail')
    email_back = forms.ChoiceField(choices=email_list, widget=forms.Select(attrs=email_attrs))
    email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs=password_attrs),
                               label='senha')
    password_conf = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs=password_conf_attrs),
                                    label='confirmar senha')

    def clean(self):

        # Checa se os campos nome e sobrenome são válidos

        nome = self.cleaned_data.get('first_name')
        sobrenome = self.cleaned_data.get('last_name')

        if nome and len(nome) < 2:
            raise forms.ValidationError(erro_cadastro['nome_incompleto'], code='nome_incompleto')

        if sobrenome and len(sobrenome) < 2:
            raise forms.ValidationError(erro_cadastro['sobrenome_incompleto'], code='sobrenome_incompleto')

        if not validar_palavra(nome):
            raise forms.ValidationError(erro_cadastro['nome_invalido'], code='nome_invalido')

        if not validar_palavra(sobrenome):
            raise forms.ValidationError(erro_cadastro['sobrenome_invalido'], code='sobrenome_invalido')

        # Checa se os campos password e password_conf estão corretos (iguais).

        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')

        if validar_senhas(password, password_conf) == 'invalida':
            raise forms.ValidationError(erro_cadastro['senha_invalida'], code='senha_invalida')

        if validar_senhas(password, password_conf) == 'diferentes':
            raise forms.ValidationError(erro_cadastro['senhas_diferentes'], code='senhas_diferentes')

        return self.cleaned_data

    def clean_email(self):

        try:
            email_front = self.cleaned_data['email_front']
            email_back = self.cleaned_data['email_back']
        except:
            raise forms.ValidationError(erro_cadastro['email_invalido'], code='email_invalido')

        email = email_front + email_back

        # Checa se o e-mail já existe.

        try:
            UsuarioModel.object.get(email=email)

        except UsuarioModel.DoesNotExist:
            return email

        raise forms.ValidationError(erro_cadastro['email_ja_existente'], code='email_ja_existente')

    class Meta:
        model = UsuarioModel
        fields = ('first_name', 'last_name', 'email_front', 'email_back', 'password', 'password_conf')


class PerfilCadastroForm(forms.ModelForm):

    # Criação dos atributos dos campos

    universidade_attrs = {'placeholder': 'Universidade', 'class': 'form-control', 'id': 'univID'}
    curso_attrs = {'placeholder': 'Curso', 'class': 'form-control', 'id': 'cursoID'}
    dia_attrs = {'class': 'form-control', 'id': 'diaID'}
    mes_attrs = {'class': 'form-control', 'id': 'mesID'}
    ano_attrs = {'class': 'form-control', 'id': 'anoID'}

    # Criação das listas de dia, mês e ano

    dia_list = [(x, str(x)) for x in range(1, 32)]
    dia_list.insert(0, (0, 'Dia'))

    mes_list = [(x, str(x)) for x in range(1, 13)]
    mes_list.insert(0, (0, 'Mês'))

    ano_list = [(x, str(x)) for x in range(datetime.today().year - 100, datetime.today().year + 1)]
    ano_list.insert(0, (0, 'Ano'))

    # Criação dos campos

    dia = forms.ChoiceField(choices=dia_list, widget=forms.Select(dia_attrs))
    mes = forms.ChoiceField(choices=mes_list, widget=forms.Select(mes_attrs))
    ano = forms.ChoiceField(choices=ano_list, widget=forms.Select(ano_attrs))

    universidade = forms.ModelChoiceField(queryset=UniversidadeModel.objects, empty_label='Universidade',
                                          label='universidade', widget=forms.Select(attrs=universidade_attrs))
    curso = forms.ModelChoiceField(queryset=CursoModel.objects, empty_label='Curso', label='curso',
                                   widget=forms.Select(attrs=curso_attrs))

    termos_condicoes = forms.BooleanField(widget=forms.CheckboxInput())

    def clean(self):

        # Checa se a os termos e condições de uso foram aceitos

        if not self.cleaned_data.get('termos_condicoes'):
            raise forms.ValidationError(erro_cadastro['termos_nao_aceitos'], code='termos_nao_aceitos')
        # Checa se a data de nascimento é válida

        dia_nasc = self.cleaned_data.get('dia')
        mes_nasc = self.cleaned_data.get('mes')
        ano_nasc = self.cleaned_data.get('ano')

        nasc_str = str(dia_nasc) + '-' + str(mes_nasc) + '-' + str(ano_nasc)

        try:
            datetime.strptime(nasc_str, '%d-%m-%Y')
        except ValueError:
            raise forms.ValidationError(erro_cadastro['data_incorreta'], code='data_incorreta')

        return self.cleaned_data

    class Meta:
        model = PerfilModel
        fields = ('dia', 'mes', 'ano', 'universidade', 'curso')


class UsuarioEditForm(forms.ModelForm):

    # Criação dos atributos dos campos

    first_name_attrs = {'placeholder': 'Nome', 'class': 'form-control', 'id': 'nomeID'}
    last_name_attrs = {'placeholder': 'Sobrenome', 'class': 'form-control', 'id': 'sobrenomeID'}

    # Criação dos campos

    first_name = forms.CharField(min_length=2, max_length=128, widget=forms.TextInput(attrs=first_name_attrs))
    last_name = forms.CharField(min_length=2, max_length=128, widget=forms.TextInput(attrs=last_name_attrs),
                                label='sobrenome')

    def clean(self):

        # Checa se os campos nome e sobrenome são válidos

        nome = self.cleaned_data.get('first_name')
        sobrenome = self.cleaned_data.get('last_name')

        if nome and len(nome) < 2:
            raise forms.ValidationError(erro_cadastro['nome_incompleto'], code='nome_incompleto')

        if sobrenome and len(sobrenome) < 2:
            raise forms.ValidationError(erro_cadastro['sobrenome_incompleto'], code='sobrenome_incompleto')

        if not validar_palavra(nome):
            raise forms.ValidationError(erro_cadastro['nome_invalido'], code='nome_invalido')

        if not validar_palavra(sobrenome):
            raise forms.ValidationError(erro_cadastro['sobrenome_invalido'], code='sobrenome_invalido')

        return self.cleaned_data

    def clean_email(self):

        try:
            email_front = self.cleaned_data['email_front']
            email_back = self.cleaned_data['email_back']
        except:
            raise forms.ValidationError(erro_cadastro['email_invalido'], code='email_invalido')

        email = email_front + email_back

        # Checa se o e-mail já existe.

        try:
            UsuarioModel.object.get(email=email)

        except UsuarioModel.DoesNotExist:
            return email

        raise forms.ValidationError(erro_cadastro['email_ja_existente'], code='email_ja_existente')

    class Meta:
        model = UsuarioModel
        fields = ('first_name', 'last_name',)


class PerfilEditForm(forms.ModelForm):

    # Criação dos atributos dos campos

    universidade_attrs = {'placeholder': 'Universidade', 'class': 'form-control', 'id': 'univID'}
    curso_attrs = {'placeholder': 'Curso', 'class': 'form-control', 'id': 'cursoID'}
    dia_attrs = {'class': 'form-control', 'id': 'diaID'}
    mes_attrs = {'class': 'form-control', 'id': 'mesID'}
    ano_attrs = {'class': 'form-control', 'id': 'anoID'}

    # Criação das listas de dia, mês e ano

    dia_list = [(x, str(x)) for x in range(1, 32)]
    dia_list.insert(0, (0, 'Dia'))

    mes_list = [(x, str(x)) for x in range(1, 13)]
    mes_list.insert(0, (0, 'Mês'))

    ano_list = [(x, str(x)) for x in range(datetime.today().year - 100, datetime.today().year + 1)]
    ano_list.insert(0, (0, 'Ano'))

    # Criação dos campos

    dia = forms.ChoiceField(choices=dia_list, widget=forms.Select(dia_attrs))
    mes = forms.ChoiceField(choices=mes_list, widget=forms.Select(mes_attrs))
    ano = forms.ChoiceField(choices=ano_list, widget=forms.Select(ano_attrs))

    universidade = forms.ModelChoiceField(queryset=UniversidadeModel.objects, empty_label='Universidade',
                                          label='universidade', widget=forms.Select(attrs=universidade_attrs))
    curso = forms.ModelChoiceField(queryset=CursoModel.objects, empty_label='Curso', label='curso',
                                   widget=forms.Select(attrs=curso_attrs))

    def clean(self):

        # Checa se a data de nascimento é válida

        dia_nasc = self.cleaned_data.get('dia')
        mes_nasc = self.cleaned_data.get('mes')
        ano_nasc = self.cleaned_data.get('ano')

        nasc_str = str(dia_nasc) + '-' + str(mes_nasc) + '-' + str(ano_nasc)

        try:
            datetime.strptime(nasc_str, '%d-%m-%Y')
        except ValueError:
            raise forms.ValidationError(erro_cadastro['data_incorreta'], code='data_incorreta')

        return self.cleaned_data

    class Meta:
        model = PerfilModel
        fields = ('dia', 'mes', 'ano', 'universidade', 'curso')


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
            email = email.lower()
            self.usuario = authenticate(username=email, password=password)

            if not self.usuario:
                # Se o usuário for nulo, então o email ou a senha estão incorretos.

                raise forms.ValidationError(erro_login['login_invalido'], code='login_invalido')

            elif not self.usuario.is_active:
                # Caso o login esteja correto, mas o usuário não esteja ativado (conta cancelada / conta não confirmada)

                raise forms.ValidationError(erro_login['email_inativo'], code='email_inativo')

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

        if email:
            email = email.lower()

        # Checa se o e-mail existe.

        try:
            UsuarioModel.object.get(email=email)

            return email
        except UsuarioModel.DoesNotExist:
            raise forms.ValidationError(erro_enviar_token['email_invalido'], code='email_invalido')

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

    senha = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs=senha_attrs),
                            label='senha', required=True)
    senha_conf = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs=senha_conf_attrs),
                                 label='confirme a senha', required=True)

    def clean(self):
        senha = self.cleaned_data.get('senha')
        senha_conf = self.cleaned_data.get('senha_conf')

        if validar_senhas(senha, senha_conf) == 'deferente':
            raise forms.ValidationError(erro_enviar_token['senhas_diferentes'], code='senhas_diferentes')

        elif validar_senhas(senha, senha_conf) == 'invalida':
            raise forms.ValidationError(erro_enviar_token['senha_invalida'], code='senha_invalida')

        return self.cleaned_data

    class Meta:
        model = UsuarioModel
        fields = ('senha', 'senha_conf')