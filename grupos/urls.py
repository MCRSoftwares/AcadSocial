# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das URLs relacionadas à aplicação de grupos e eventos.
"""

from django.conf.urls import patterns, url
from grupos import views


urlpatterns = patterns('',
                       url(r'^grupos/lista/$', views.view_lista_grupos, name='grupos-lista'),
                       url(r'^grupos/(?P<gid>\w+)/$', views.view_pagina_grupo, name='grupo-index'),
                       url(r'^grupos/(?P<gid>\w+)/editar/$', views.view_editar_grupo, name='grupo-editar'),
                       url(r'^grupos/(?P<gid>\w+)/entrar/$', views.view_entrar_grupo, name='grupo-entrar'),
                       url(r'^interesses/$', views.view_interesses, name='interesses'),
                       url(r'^interesses/(?P<iid>\w+)/$', views.view_pagina_interesse, name='interesse-index'),
                       )