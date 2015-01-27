# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v004a

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
                       url(r'^admin/', include(admin.site.urls), name='admin'),
                       url(r'^', include('contas.urls')),
                       url(r'^', include('mainAcad.urls')),
                       url(r'^', include('grupos.urls')),
                       )

handler404 = 'mainAcad.views.custom_404'
handler500 = 'mainAcad.views.custom_500'
if settings.DEBUG:
    urlpatterns += patterns('django.views.static', (r'media/(?P<path>.*)', 'serve',
                                                    {'document_root': settings.MEDIA_ROOT}))