# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das páginas do admin relacionadas à aplicação de universidades.
"""

from django.contrib import admin
from universidades.models import UniversidadeModel, CursoModel

admin.site.register(UniversidadeModel)
admin.site.register(CursoModel)
