# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

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
from contas.models import UsuarioModel, PerfilModel
from contas.forms import UsuarioChangeForm, UsuarioCreationForm


class UsuarioAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),)
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class PerfilAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('User info'), {'fields': ('usuario',)}),
        (_('Personal info'), {'fields': ('universidade', 'curso', 'foto', 'data_nascimento')}),
    )

    list_display = ('usuario', 'universidade', 'curso')
    search_fields = ('universidade', 'curso',)


admin.site.register(UsuarioModel, UsuarioAdmin)
admin.site.register(PerfilModel, PerfilAdmin)