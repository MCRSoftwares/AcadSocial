# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição dos formulários relacionados à aplicação de grupos e eventos.
"""

from django import forms
from grupos.errors import erro_interesse
from grupos.models import ComentarioGrupoModel, InteresseModel


class ComentarioGrupoForm(forms.ModelForm):

    class Meta:
        model = ComentarioGrupoModel
        fields = ()


class InteresseSearchForm(forms.ModelForm):

    pesquisa_attrs = {
        'placeholder': 'Pesquisar Interesse...',
        'class': 'form-control search-bar-interesse',
        'id': 'interesseQry',
        'autocomplete': 'off',
    }

    iq = forms.CharField(max_length=128, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = InteresseModel
        fields = ('iq', )


class AdicionarInteresseForm(forms.ModelForm):

    interesse_attrs = {
        'placeholder': 'Nomear Interesse...',
        'class': 'form-control search-bar-interesse',
        'id': 'interesseField',
        'autocomplete': 'off',
    }

    criarInteresse = forms.CharField(max_length=128, widget=forms.HiddenInput(attrs=interesse_attrs))

    def clean(self):
        interesse = self.cleaned_data.get('criarInteresse')

        if not interesse or not ''.join(unicode(interesse).split()):
            raise forms.ValidationError(erro_interesse['interesse_invalido'], code='interesse_invalido')

        while unicode(interesse).startswith(' '):
            interesse = interesse[1:]

        interesse = interesse.lower()

        try:
            InteresseModel.objects.get(interesse=interesse)

            raise forms.ValidationError(erro_interesse['interesse_ja_existente'], code='interesse_ja_existente')
        except InteresseModel.DoesNotExist:
            return self.cleaned_data

    class Meta:
        model = InteresseModel
        fields = ('criarInteresse', )