# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

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


@register.filter(name="first_five")
def get_first_five(dictionary, key):
    return dictionary.get(key)[:5]


@register.filter(name="get_interesses")
def get_interesse_in(lista):
    interesses = []

    for valor in lista:
        interesses.append(valor.interesse)

    return interesses


@register.filter(name="get_grupos")
def get_grupo_in(lista):
    grupos = []

    for valor in lista:
        grupos.append(valor.grupo)

    return grupos


@register.filter(name="get_convite")
def is_convidado_in(lista, usuario):
    usuarios = []

    for valor in lista:
        usuarios.append(valor.convidado)

    if usuario in usuarios:
        return True

    return False


@register.filter(name="is_member")
def get_membro_check(membros, usuario):

    for membro in membros:
        if usuario is membro.usuario:
            return True

    return False