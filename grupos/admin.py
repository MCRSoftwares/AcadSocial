# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

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
from grupos.models import ConviteEventoModel, ConviteGrupoModel
from grupos.models import ComentarioGrupoModel, ComentarioEventoModel, PostagemEventoModel, PostagemGrupoModel
from django.utils.translation import ugettext_lazy as _


class GrupoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do grupo'), {'fields': ('nome', 'descricao',)}),
        (_(u'Criação'), {'fields': ('criado_por', 'data_criacao')}),
    )

    list_display = ('nome', 'descricao', 'criado_por', 'data_criacao')
    search_fields = ('criado_por', 'nome', 'descricao',)


class EventoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do evento'), {'fields': ('titulo', 'descricao', 'data_evento', 'grupo')}),
        (_(u'Criação'), {'fields': ('criado_por', 'data_criacao')}),
    )

    list_display = ('titulo', 'descricao', 'criado_por', 'data_criacao')
    search_fields = ('criado_por', 'titulo', 'descricao',)


class InteresseAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do interesse'), {'fields': ('interesse', 'criado_por', 'data_criacao',)}),
    )

    list_display = ('interesse', 'criado_por', 'data_criacao',)
    search_fields = ('interesse', 'criado_por', 'data_criacao',)


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


class ConviteGrupoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Usuários relacionados'), {'fields': ('usuario', 'convidado',)}),
        (_(u'Informações do convite'), {'fields': ('grupo', 'data_envio', 'ativo', 'aceito',)}),
    )

    list_display = ('grupo', 'usuario', 'convidado', 'data_envio', 'aceito', 'ativo',)
    search_fields = ('grupo', 'usuario', 'convidado', 'data_envio',)


class ConviteEventoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Usuários relacionados'), {'fields': ('usuario', 'convidado',)}),
        (_(u'Informações do convite'), {'fields': ('evento', 'data_envio', 'ativo', 'aceito',)}),
    )

    list_display = ('evento', 'usuario', 'convidado', 'data_envio', 'aceito', 'ativo',)
    search_fields = ('evento', 'usuario', 'convidado', 'data_envio',)


class PostagemGrupoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('criado_por',)}),
        (_(u'Informações da postagem'), {'fields': ('ativo', 'grupo',
                                                    'titulo', 'conteudo', 'data_criacao',)}),
    )

    list_display = ('grupo', 'criado_por', 'data_criacao', 'ativo',)
    search_fields = ('ativo', 'grupo', 'titulo', 'conteudo', 'data_criacao', 'criado_por',)


class PostagemEventoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('criado_por',)}),
        (_(u'Informações da postagem'), {'fields': ('ativo', 'grupo', 'evento',
                                                    'titulo', 'conteudo', 'data_criacao',)}),
    )

    list_display = ('grupo', 'evento', 'criado_por', 'data_criacao', 'ativo',)
    search_fields = ('ativo', 'grupo', 'evento', 'titulo', 'conteudo', 'data_criacao', 'criado_por',)


class ComentarioGrupoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('criado_por',)}),
        (_(u'Informações do comentário'), {'fields': ('ativo', 'postagem',
                                                      'conteudo', 'data_criacao',)}),
    )

    list_display = ('postagem', 'criado_por', 'data_criacao', 'ativo',)
    search_fields = ('ativo', 'postagem', 'conteudo', 'data_criacao', 'criado_por',)


class ComentarioEventoAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('criado_por',)}),
        (_(u'Informações do comentário'), {'fields': ('ativo', 'postagem',
                                                      'conteudo', 'data_criacao',)}),
    )

    list_display = ('postagem', 'criado_por', 'data_criacao', 'ativo',)
    search_fields = ('ativo', 'postagem', 'conteudo', 'data_criacao', 'criado_por',)


admin.site.register(GrupoModel, GrupoAdmin)
admin.site.register(EventoModel, EventoAdmin)
admin.site.register(InteresseModel, InteresseAdmin)
admin.site.register(MembroModel, MembroAdmin)
admin.site.register(ParticipaEventoModel, ParticipaEventoAdmin)
admin.site.register(UsuarioInteresseModel, UsuarioInteresseAdmin)
admin.site.register(GrupoInteresseModel, GrupoInteresseAdmin)
admin.site.register(ConviteGrupoModel, ConviteGrupoAdmin)
admin.site.register(ConviteEventoModel, ConviteEventoAdmin)
admin.site.register(PostagemGrupoModel, PostagemGrupoAdmin)
admin.site.register(PostagemEventoModel, PostagemEventoAdmin)
admin.site.register(ComentarioGrupoModel, ComentarioGrupoAdmin)
admin.site.register(ComentarioEventoModel, ComentarioEventoAdmin)
