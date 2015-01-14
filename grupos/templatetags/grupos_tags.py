# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das tags customizadas para utilizar nos templates de grupos.
"""

from django import template

register = template.Library()


@register.filter(name="item")
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name="perfil_link")
def get_perfil_link(dictionary, key):
    return dictionary.get(key).perfil_link


@register.filter(name="univ_sigla")
def get_univ_sigla(dictionary, key):
    return dictionary.get(key).universidade.sigla