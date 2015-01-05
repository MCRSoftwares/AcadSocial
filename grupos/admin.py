# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

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


class EventoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do evento'), {'fields': ('titulo', 'descricao')}),
        (_(u'Criação'), {'fields': ('criado_por', 'data_criacao')}),
    )

    list_display = ('titulo', 'descricao', 'criado_por', 'data_criacao')
    search_fields = ('criado_por', 'titulo', 'descricao',)


class InteresseAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do interesse'), {'fields': ('interesse', 'data_criacao',)}),
    )

    list_display = ('interesse', 'data_criacao',)
    search_fields = ('interesse', 'data_criacao',)


class MembroAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do membro'), {'fields': ('usuario', 'grupo', 'data_entrada', 'is_admin')}),
    )

    list_display = ('usuario', 'grupo', 'data_entrada', 'is_admin',)
    search_fields = ('usuario', 'grupo', 'data_entrada', 'is_admin',)


class ParticipaEventoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações da relação'), {'fields': ('usuario', 'evento', 'data_participacao')}),
    )

    list_display = ('evento', 'usuario', 'data_participacao',)
    search_fields = ('evento', 'usuario', 'data_participacao',)


class UsuarioInteresseAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações da relação'), {'fields': ('usuario', 'interesse', 'data_criacao')}),
    )

    list_display = ('interesse', 'usuario', 'data_criacao',)
    search_fields = ('interesse', 'usuario', 'data_criacao',)


class GrupoInteresseAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações da relação'), {'fields': ('grupo', 'interesse', 'data_criacao')}),
    )

    list_display = ('interesse', 'grupo', 'data_criacao',)
    search_fields = ('interesse', 'grupo', 'data_criacao',)


admin.site.register(GrupoModel, GrupoAdmin)
admin.site.register(EventoModel, EventoAdmin)
admin.site.register(InteresseModel, InteresseAdmin)
admin.site.register(MembroModel, MembroAdmin)
admin.site.register(ParticipaEventoModel, ParticipaEventoAdmin)
admin.site.register(UsuarioInteresseModel, UsuarioInteresseAdmin)
admin.site.register(GrupoInteresseModel, GrupoInteresseAdmin)
