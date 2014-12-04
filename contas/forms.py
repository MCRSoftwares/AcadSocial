# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v01a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição dos formulários relacionados à aplicação de contas (cadastro/login).
"""

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from contas.models import UsuarioModel, PerfilModel
from django import forms
from datetime import datetime
from contas import errors

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


# Forms relacionados à views.py


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
            raise forms.ValidationError(errors.erro_senhas_diferentes)

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            UsuarioModel.object.get(email=email)

        except UsuarioModel.DoesNotExist:
            return email

        raise forms.ValidationError(errors.erro_email_ja_existe)

    class Meta:
        model = UsuarioModel
        fields = ('first_name', 'last_name', 'email', 'password', 'password_conf')


class PerfilCadastroForm(forms.ModelForm):

    # Criação dos atributos dos campos

    universidade_attrs = {'placeholder': 'Universidade'}
    campus_attrs = {'placeholder': 'Campus'}
    curso_attrs = {'placeholder': 'Curso'}

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

    # TODO alterar os campos abaixo para ChoiceField, após criação do banco de cursos/campus da UFPE

    universidade = forms.CharField(max_length=256, widget=forms.TextInput(attrs=universidade_attrs))
    campus = forms.CharField(max_length=256, widget=forms.TextInput(attrs=campus_attrs))
    curso = forms.CharField(max_length=256, widget=forms.TextInput(attrs=curso_attrs))

    def clean(self):

        # Checa se a data de nascimento é válida

        dia_nasc = self.cleaned_data.get('dia')
        mes_nasc = self.cleaned_data.get('mes')
        ano_nasc = self.cleaned_data.get('ano')

        nasc_str = str(dia_nasc) + '-' + str(mes_nasc) + '-' + str(ano_nasc)

        try:
            datetime.strptime(nasc_str, '%d-%m-%Y')
        except ValueError:
            raise forms.ValidationError(errors.erro_data_incorreta)

    class Meta:
        model = PerfilModel
        fields = ('dia', 'mes', 'ano', 'universidade', 'curso', 'campus', 'foto')