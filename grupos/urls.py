# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das URLs relacionadas à aplicação de grupos e eventos.
"""

from django.conf.urls import patterns, include, url
from grupos import views


urlpatterns = patterns('',
                       url(r'^(?P<gid>\w+)/', views.view_pagina_grupo, name='grupo-index'),
                       )