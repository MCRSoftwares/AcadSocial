# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das páginas do admin relacionadas à aplicação de universidades.
"""

from django.contrib import admin
from universidades.models import UniversidadeModel, CursoModel
from django.utils.translation import ugettext_lazy as _


class UniversidadeAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('Info'), {'fields': ('sigla', 'nome', 'campus')}),
    )
    
    list_display = ('sigla', 'nome', 'campus')
    search_fields = ('sigla', 'nome', 'campus')
    ordering = ('sigla',)


class CursoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('Info'), {'fields': ('nome', 'universidade')}),
    )
    
    list_display = ('nome', 'universidade')
    search_fields = ('nome', 'universidade', 'campus')
    ordering = ('nome',)

admin.site.register(UniversidadeModel, UniversidadeAdmin)
admin.site.register(CursoModel, CursoAdmin)
