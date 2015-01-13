# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das views relacionadas à aplicação de grupos e eventos.
"""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from grupos.models import GrupoModel, MembroModel
from django.contrib.auth.decorators import login_required
from mainAcad.models import ImagemModel
from mainAcad.forms import UsuarioSearchForm
from contas.models import PerfilModel
from grupos.models import InteresseModel


@login_required
def view_pagina_grupo(request, gid):
    args = {}
    grupo = None

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        membro = MembroModel.objects.get(grupo=grupo, usuario=request.user)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        membro = None

    args['membro'] = membro
    args['grupo'] = grupo
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)
    args['perfil'] = PerfilModel.objects.get(usuario=request.user)

    return render(request, 'grupos/pagina_grupo.html', args)


@login_required
def view_editar_grupo(request, gid):
        args = {}

        try:
            grupo = GrupoModel.objects.get(gid=gid)
            membro = MembroModel.objects.get(is_admin=True, grupo=grupo, usuario=request.user)

        except GrupoModel.DoesNotExist:
            return HttpResponseRedirect('/')

        except MembroModel.DoesNotExist:
            return HttpResponseRedirect('/grupo/' + gid + '/')

        return render(request, 'grupos/editar_grupo.html', args)


@login_required
def view_entrar_grupo(request, gid):

    grupo = None

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        MembroModel.objects.get(usuario=request.user, grupo=grupo)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        membro = MembroModel(usuario=request.user, grupo=grupo)
        membro.save()

    return HttpResponseRedirect('/grupo/' + gid + '/')


@login_required
def view_lista_grupos(request):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)

    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    return render(request, 'grupos/lista_grupos.html', args)


@login_required
def view_pagina_interesse(request, iid):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    interesse = InteresseModel.objects.get(iid=iid)

    args['interesse'] = interesse
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    return render(request, 'grupos/interesse.html', args)


def view_interesses(request):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)

    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    return render(request, 'grupos/lista_interesses.html', args)