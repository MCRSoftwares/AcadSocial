# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das URLs relacionadas à aplicação principal.
"""

from django.conf.urls import patterns, include, url

from mainAcad import views

urlpatterns = patterns('',

                       url(r'search/$', views.view_usuario_search, name='search'),
                       url(r'bugs/$', views.view_reportar_bug, name='bugs'),
                       url(r'contato/$', views.view_fale_conosco, name='contato'),
                       url(r'denuncia/$', views.view_denuncia, name='denuncia'),
                       )
