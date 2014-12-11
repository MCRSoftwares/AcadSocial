# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v004a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das páginas do admin relacionadas à aplicação de contas (cadastro/login).
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from contas.models import UsuarioModel, PerfilModel, TokenModel
from contas.forms import UsuarioChangeForm, UsuarioCreationForm


class UsuarioAdmin(UserAdmin):

    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'full_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),)
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)


class PerfilAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('usuario', 'perfil_link',)}),
        (_('Personal info'), {'fields': ('universidade', 'curso', 'foto', 'data_nascimento')}),
    )

    list_display = ('usuario', 'perfil_link', 'universidade', 'curso',)
    search_fields = ('usuario__email', 'perfil_link', 'universidade__sigla', 'curso__nome',)


class TokenAdmin(admin.ModelAdmin):

    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('usuario',)}),
        (_('Token'), {'fields': ('active', 'valid', 'token', 'tipo', 'data_expiracao', 'data_request')}),
    )

    list_display = ('usuario', 'data_expiracao', 'data_request', 'tipo', 'active', 'valid')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'usuario__email', 'tipo',)


admin.site.register(UsuarioModel, UsuarioAdmin)
admin.site.register(PerfilModel, PerfilAdmin)
admin.site.register(TokenModel, TokenAdmin)