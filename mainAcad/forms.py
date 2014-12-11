# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição dos forms relacionadas à aplicação principal.
"""

from django import forms
from contas.models import UsuarioModel


class UsuarioSearchForm(forms.ModelForm):

    pesquisa_attrs = {'placeholder': 'Pesquisar...', 'class': 'form-control'}

    pesquisa = forms.CharField(max_length=256, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = UsuarioModel
        fields = ()