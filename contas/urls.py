# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002, RF020, RF022, RF023, RF027
Caso(s) de Uso: DV001, DV002, DVA012

Descrição:
    Definição das URLs relacionadas à aplicação de contas (cadastro/login).
"""

from django.conf.urls import patterns, include, url

from contas import views

urlpatterns = patterns('',
                       url(r'^$', views.view_pagina_inicial, name='index'),

                       url(r'^conta/cadastro/$', views.view_cadastrar_usuario, name='cadastro'),
                       url(r'^conta/ativar/(?P<chave>\w+)/', views.view_confirmar_usuario, name='confirmar'),
                       url(r'^conta/reativar/', views.view_reativar_usuario, name='reativar'),
                       url(r'^perfil/(?P<sigla>\w+)/(?P<perfil_link>[\w\-]+)/$',
                           views.view_perfil_usuario, name='perfil'),
                       url(r'^perfil/(?P<sigla>\w+)/(?P<perfil_link>[\w\-]+)/sobre/$',
                           views.view_perfil_usuario_sobre, name='perfil-sobre'),

                       url(r'^conta/login/', views.view_login_usuario, name='login'),
                       url(r'^conta/logout/', views.view_logout_usuario, name='logout'),

                       url(r'^conta/senha/reset/$', views.view_senha_reset, name='senha-reset'),
                       url(r'^conta/senha/(?P<uid>\w+)/(?P<chave>\w+)/', views.view_senha_reset_confirmado,
                           name='senha-reset-confirmado'),
                       )
