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
from grupos.models import ComentarioGrupoModel


class ComentarioGrupoForm(forms.ModelForm):

    class Meta:
        model = ComentarioGrupoModel
        fields = ()