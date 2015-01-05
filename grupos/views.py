# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das views relacionadas à aplicação de grupos e eventos.
"""

from django.shortcuts import render


def view_pagina_grupo(request, gid):
    args = {}
    # TODO criar view das páginas dos grupos
    return render(request, 'grupos/pagina_grupo.html', args)
