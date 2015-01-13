# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

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

                       url(r'search/', views.view_usuario_search, name='search'),
                       url(r'^amigos/$', views.view_lista_amigos, name='amigos'),
                       )
