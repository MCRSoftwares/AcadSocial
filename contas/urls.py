# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das URLs relacionadas à aplicação de contas (cadastro/login).
"""

from django.conf.urls import patterns, include, url
from contas import views

urlpatterns = patterns('',
                       url(r'^$', views.view_pagina_inicial, name='index'),
                       url(r'^cadastro/$', views.view_cadastrar_usuario, name='cadastro'),
                       url(r'^perfil/ativar/(?P<chave>\w+)/', views.view_confirmar_usuario, name='confirmar'),
                       url(r'^login/', views.view_login_usuario, name='login'),
                       )
