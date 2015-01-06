# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das views relacionadas à aplicação principal.
"""

from django.shortcuts import render
from mainAcad.forms import UsuarioSearchForm
from contas.models import PerfilModel, UsuarioModel
from grupos.models import GrupoModel
from universidades.models import UniversidadeModel, CursoModel
from django.db.models import Q


def view_usuario_search(request):
    args = {}

    # TODO criar uma forma de pesquisa completa (esta serve somente para resgatar perfil de usuários)
    # TODO alterar forma em que os dados são salvos: tudo em lowerCase, para ajudar na pesquisa.

    if request.GET.items():
        pesquisa_form = UsuarioSearchForm(data=request.GET)

        if pesquisa_form.is_valid():
            data = pesquisa_form.cleaned_data['pesquisa']

            perfil_query = Q(usuario__full_name__contains=data) | Q(perfil_link__contains=data)

            univ_query = Q(sigla__contains=data) | Q(nome__contains=data)

            curso_query = Q(nome__contains=data) | Q(universidade__sigla__contains=data) | \
                Q(universidade__nome__contains=data)

            grupo_query = Q(nome__contains=data) | Q(grupointeressemodel__interesse__interesse__contains=data)

            perfils = PerfilModel.objects.filter(perfil_query, usuario__is_active=True)
            universidades = UniversidadeModel.objects.filter(univ_query)
            cursos = CursoModel.objects.filter(curso_query)
            grupos = GrupoModel.objects.filter(grupo_query)

            args['perfils'] = perfils
            args['universidades'] = universidades
            args['cursos'] = cursos
            args['grupos'] = grupos
    else:
        pesquisa_form = UsuarioSearchForm()

    args['pesquisa_form'] = pesquisa_form

    return render(request, 'mainAcad/search.html', args)