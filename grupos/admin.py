# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF004, RF005, RF007, RF006
Caso(s) de Uso: DVA001, DVA002, DVA006, DVA007

Descrição:
    Definição das páginas do admin relacionadas à aplicação de grupos e eventos.
"""

from django.contrib import admin
from grupos.models import GrupoModel, EventoModel, MembroModel, ParticipaEventoModel
from grupos.models import InteresseModel, UsuarioInteresseModel, GrupoInteresseModel
from django.utils.translation import ugettext_lazy as _


class GrupoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do grupo'), {'fields': ('nome', 'descricao')}),
        (_(u'Criação'), {'fields': ('criado_por', 'data_criacao')}),
    )

    list_display = ('nome', 'descricao', 'criado_por', 'data_criacao')
    search_fields = ('criado_por', 'nome', 'descricao',)

admin.site.register(GrupoModel, GrupoAdmin)
admin.site.register(EventoModel)
admin.site.register(InteresseModel)
admin.site.register(MembroModel)
admin.site.register(ParticipaEventoModel)
admin.site.register(UsuarioInteresseModel)
admin.site.register(GrupoInteresseModel)
