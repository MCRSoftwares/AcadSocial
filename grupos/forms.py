# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição dos formulários relacionados à aplicação de grupos e eventos.
"""

from django import forms
from grupos.errors import erro_interesse, erro_grupo
from grupos.models import ComentarioGrupoModel, InteresseModel, GrupoModel, PostagemGrupoModel
from grupos.models import ComentarioEventoModel, PostagemEventoModel


class ComentarioGrupoForm(forms.ModelForm):

    class Meta:
        model = ComentarioGrupoModel
        fields = ()


class ComentarioEventoForm(forms.ModelForm):

    class Meta:
        model = ComentarioEventoModel
        fields = ()


class InteresseSearchForm(forms.ModelForm):

    pesquisa_attrs = {
        'placeholder': 'Criar/Pesquisar Interesses...',
        'class': 'form-control search-bar-interesse',
        'id': 'interesseQry',
        'autocomplete': 'off',
    }

    iq = forms.CharField(max_length=64, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = InteresseModel
        fields = ('iq', )


class AdicionarInteresseForm(forms.ModelForm):

    interesse_attrs = {
        'id': 'interesseField',
    }

    criarInteresse = forms.CharField(max_length=64, widget=forms.HiddenInput(attrs=interesse_attrs))

    def clean(self):
        interesse = self.cleaned_data.get('criarInteresse')
        interesse = ' '.join(unicode(interesse).split())

        if not interesse or not ''.join(unicode(interesse).split()):
            raise forms.ValidationError(erro_interesse['interesse_invalido'], code='interesse_invalido')

        if unicode(interesse).startswith(' '):
            interesse = interesse[1:]

        try:
            InteresseModel.objects.get(interesse__iexact=interesse)

            raise forms.ValidationError(erro_interesse['interesse_ja_existente'], code='interesse_ja_existente')
        except InteresseModel.DoesNotExist:
            return self.cleaned_data

    class Meta:
        model = InteresseModel
        fields = ('criarInteresse', )


class GrupoSearchForm(forms.ModelForm):

    pesquisa_attrs = {
        'placeholder': 'Criar/Pesquisar Grupos...',
        'class': 'form-control search-bar-interesse',
        'id': 'grupoQry',
        'autocomplete': 'off',
    }

    gq = forms.CharField(max_length=64, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = GrupoModel
        fields = ('gq', )


class AdicionarGrupoForm(forms.ModelForm):

    grupo_attrs = {
        'id': 'grupoField'
    }

    criarGrupo = forms.CharField(max_length=64, widget=forms.HiddenInput(attrs=grupo_attrs))

    def clean(self):
        grupo = self.cleaned_data.get('criarGrupo')
        grupo = ' '.join(unicode(grupo).split())

        if not grupo or not ''.join(unicode(grupo).split()):
            raise forms.ValidationError(erro_grupo['grupo_invalido'], code='grupo_invalido')

        if unicode(grupo).startswith(' '):
            grupo = grupo[1:]

        try:
            GrupoModel.objects.get(nome__iexact=grupo)

            raise forms.ValidationError(erro_grupo['grupo_ja_existente'], code='grupo_ja_existente')
        except GrupoModel.DoesNotExist:
            return self.cleaned_data

    class Meta:
        model = GrupoModel
        fields = ('criarGrupo', )


class PostagemGrupoForm(forms.ModelForm):

    titulo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Título...',
    }

    conteudo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Conteúdo...',
        'maxlength': '256',
        'rows': '1',
    }

    titulo = forms.CharField(max_length=32, widget=forms.TextInput(attrs=titulo_attrs), required=True)
    conteudo = forms.CharField(widget=forms.Textarea(attrs=conteudo_attrs), required=True)

    class Meta:
        model = PostagemGrupoModel
        fields = ('titulo', 'conteudo', )


class PostagemEventoForm(forms.ModelForm):

    titulo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Título...',
    }

    conteudo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Conteúdo...',
        'maxlength': '256',
        'rows': '1',
    }

    titulo = forms.CharField(max_length=32, widget=forms.TextInput(attrs=titulo_attrs), required=True)
    conteudo = forms.CharField(widget=forms.Textarea(attrs=conteudo_attrs), required=True)

    class Meta:
        model = PostagemEventoModel
        fields = ('titulo', 'conteudo', )


class MembroSearchForm(forms.ModelForm):

    pesquisa_attrs = {
        'placeholder': 'Pesquisar Usuários...',
        'class': 'form-control search-bar-interesse',
        'id': 'usuarioQry',
        'autocomplete': 'off',
    }

    aq = forms.CharField(max_length=64, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = GrupoModel
        fields = ('aq', )