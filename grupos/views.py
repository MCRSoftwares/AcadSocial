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
from django.http import HttpResponseRedirect
from grupos.models import GrupoModel, MembroModel
from contas.models import UsuarioModel
from django.contrib.auth.decorators import login_required


@login_required
def view_pagina_grupo(request, gid):
    args = {}

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        membro = MembroModel.objects.get(grupo=grupo, usuario=request.user)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        membro = None

    args['membro'] = membro

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