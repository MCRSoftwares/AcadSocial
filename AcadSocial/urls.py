# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das URLs do sistema em geral.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('contas.urls')),
                       )

if settings.DEBUG:
    urlpatterns += patterns('django.views.static', (r'media/(?P<path>.*)', 'serve',
                                                    {'document_root': settings.MEDIA_ROOT}))