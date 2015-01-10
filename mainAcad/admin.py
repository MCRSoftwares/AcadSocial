# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das páginas do admin relacionadas à aplicação principal.
"""

from django.contrib import admin
from mainAcad.models import ImagemModel
from django.utils.translation import ugettext_lazy as _


class ImagemAdmin(admin.ModelAdmin):
    fieldsets = (
        (_(u'Informações do usuário'), {'fields': ('perfil',)}),
        (_('Image'), {'fields': ('is_active', 'is_profile_image', 'imagem', 'thumbnail', 'thumbnail_home',
                                 'thumbnail_perfil', 'data_envio')}),
    )

    list_display = ('perfil', 'imagem', 'data_envio', 'is_profile_image', 'is_active')
    search_fields = ('perfil__usuario__first_name', 'perfil__usuario__last_name',
                     'perfil__usuario__email', 'data_envio',)


admin.site.register(ImagemModel, ImagemAdmin)