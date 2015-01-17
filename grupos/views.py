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

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from grupos.models import GrupoModel, MembroModel
from django.contrib.auth.decorators import login_required
from mainAcad.models import ImagemModel
from mainAcad.forms import UsuarioSearchForm
from contas.models import PerfilModel
from grupos.models import InteresseModel, PostagemGrupoModel, ComentarioGrupoModel, UsuarioInteresseModel
from grupos.forms import ComentarioGrupoForm, AdicionarInteresseForm, InteresseSearchForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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


@login_required
def view_interesses(request):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    perfil_interesses = UsuarioInteresseModel.objects.filter(usuario=perfil.usuario)

    interesses = []

    if request.GET.get('iq'):
        processed_data = ['da2sipg34xlc4a5fop4rek5u2']
        lista = request.GET.get('iq').split(' ')
        data_list = filter(None, lista)

        args['data_list'] = request.GET.get('iq')

        for data in data_list:

            if data not in processed_data:

                try:
                    query = InteresseModel.objects.filter(interesse__contains=data)
                    interesses = interesses + list(query)

                    if query:
                        processed_data.append(data)

                except InteresseModel.DoesNotExist:
                    pass

        interesses = list(set(interesses))

        args['data'] = processed_data

    if request.method == 'POST':

        if 'criarInteresse' in request.POST:
            interesse_form = AdicionarInteresseForm(data=request.POST)

            if interesse_form.is_valid():
                interesse = interesse_form.save(commit=False)

                interesse.interesse = interesse_form.cleaned_data['criarInteresse']
                interesse.criado_por = request.user
                interesse.save()

                usuario_interesse = UsuarioInteresseModel()
                usuario_interesse.interesse = interesse
                usuario_interesse.usuario = request.user
                usuario_interesse.save()

                return HttpResponseRedirect('/interesse/')

        if 'addInteresse' in request.POST:
            interesse_id = request.POST.get('addInteresse')
            interesse_obj = InteresseModel.objects.get(iid=interesse_id)

            usuario_interesse = UsuarioInteresseModel()
            usuario_interesse.interesse = interesse_obj
            usuario_interesse.usuario = request.user
            usuario_interesse.save()

            return HttpResponseRedirect('/interesse/')

    else:
        interesse_form = AdicionarInteresseForm()

    args['pesquisa_interesse_form'] = InteresseSearchForm()
    args['interesse_form'] = interesse_form
    args['perfil_interesses'] = perfil_interesses
    args['interesses'] = interesses
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm()

    return render(request, 'grupos/lista_interesses.html', args)


@login_required
def view_postagem_grupo(request, gid, pid):
    args = {}

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        MembroModel.objects.get(grupo=grupo, usuario=request.user)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        return HttpResponseRedirect('/grupo/' + gid + '/')

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    postagem = get_object_or_404(PostagemGrupoModel, grupo__gid=gid, pid=pid, ativo=True)
    comentarios = ComentarioGrupoModel.objects.filter(postagem=postagem,
                                                      ativo=True).order_by('-data_criacao')

    foto_postagem = ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                            perfil__usuario=postagem.criado_por).thumbnail_perfil
    perfil_postagem = PerfilModel.objects.get(usuario=postagem.criado_por)

    fotos_comentarios = {}
    perfis_comentarios = {}

    qtd_comentarios = len(comentarios)
    paginas = Paginator(comentarios, 10)

    for comentario in comentarios:
        if comentario.criado_por not in fotos_comentarios:
            fotos_comentarios[comentario.criado_por] = \
                ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                        perfil__usuario=comentario.criado_por).thumbnail

        if comentario.criado_por not in perfis_comentarios:
            perfis_comentarios[comentario.criado_por] = PerfilModel.objects.get(usuario=comentario.criado_por)

    if request.method == 'GET':
        pagina = request.GET.get('page')

        try:
            comentarios = paginas.page(pagina)
        except PageNotAnInteger:
            comentarios = paginas.page(1)
        except EmptyPage:
            comentarios = paginas.page(paginas.num_pages)

    if request.method == 'POST':

        if 'deleteComment' in request.POST:
            cid = int(request.POST['deleteComment'])

            try:
                custom_query = Q(criado_por=request.user) | Q(criado_por=postagem.criado_por)
                comentario = ComentarioGrupoModel.objects.get(Q(postagem__pid=pid), Q(cid=cid), custom_query)
                comentario.ativo = False
                comentario.save()

            except ComentarioGrupoModel.DoesNotExist:
                pass

        if 'deletePost' in request.POST:

            try:
                postagem.ativo = False
                postagem.save()

                return HttpResponseRedirect('/grupo/' + gid)

            except PostagemGrupoModel.DoesNotExist:
                pass

        if 'comment' in request.POST:
            comentario_form = ComentarioGrupoForm(data=request.POST)

            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)

                comentario.criado_por = request.user
                comentario.conteudo = request.POST['comentario']
                comentario.postagem = postagem
                comentario.data_criacao = timezone.now()
                comentario.save()

        return HttpResponseRedirect('/grupo/' + gid + '/post/' + pid)

    else:
        comentario_form = ComentarioGrupoForm()

    args['qtd_comentarios'] = qtd_comentarios
    args['comentario_form'] = comentario_form
    args['comentarios'] = comentarios
    args['postagem'] = postagem
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    args['perfil_postagem'] = perfil_postagem
    args['foto_postagem'] = foto_postagem
    args['perfis_comentarios'] = perfis_comentarios
    args['fotos_comentarios'] = fotos_comentarios

    return render(request, 'grupos/postagem.html', args)