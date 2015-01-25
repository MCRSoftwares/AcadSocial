# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v008a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das views relacionadas à aplicação de grupos e eventos.
"""

# TODO Configurar views que possuem notificações

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from grupos.models import GrupoModel, MembroModel
from django.contrib.auth.decorators import login_required
from mainAcad.models import ImagemModel, AmigoModel
from mainAcad.forms import UsuarioSearchForm
from contas.models import PerfilModel, UsuarioModel
from grupos.models import InteresseModel, PostagemGrupoModel, ComentarioGrupoModel, EventoModel, ParticipaEventoModel
from grupos.models import UsuarioInteresseModel, GrupoInteresseModel, ConviteGrupoModel, ConviteEventoModel
from grupos.models import PostagemEventoModel, ComentarioEventoModel
from grupos.forms import ComentarioGrupoForm, AdicionarInteresseForm, InteresseSearchForm, PostagemEventoForm
from grupos.forms import GrupoSearchForm, AdicionarGrupoForm, PostagemGrupoForm, MembroSearchForm, ComentarioEventoForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from grupos.methods import load_convites_amigos, load_convites_eventos, load_convites_grupos
from grupos.methods import convites_amigos_post, convites_grupos_post, convites_eventos_post


@login_required
def view_pagina_grupo(request, gid):
    args = {}
    grupo = None

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        membro = MembroModel.objects.get(grupo=grupo, usuario=request.user, ativo=True)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        membro = None

    membros = MembroModel.objects.filter(grupo=grupo, ativo=True)
    postagens = PostagemGrupoModel.objects.filter(grupo=grupo, ativo=True).order_by('-data_criacao')
    comentarios = ComentarioGrupoModel.objects.filter(postagem__in=postagens, ativo=True)
    interesses = GrupoInteresseModel.objects.filter(grupo=grupo)

    qtd_postagens = len(postagens)

    comentario_postagem = {}
    fotos_comentarios = {}
    fotos_postagens = {}
    perfis_comentarios = {}
    perfis_postagens = {}
    qtd_comentarios = {}
    usuarios = {}

    for comentario in comentarios:
        if comentario.criado_por not in fotos_comentarios:
            fotos_comentarios[comentario.criado_por] = \
                ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                        perfil__usuario=comentario.criado_por).thumbnail

        if comentario.criado_por not in perfis_comentarios:
            perfis_comentarios[comentario.criado_por] = PerfilModel.objects.get(usuario=comentario.criado_por)

    for postagem in postagens:
        if postagem.criado_por not in fotos_postagens:
            fotos_postagens[postagem.criado_por] = \
                ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                        perfil__usuario=postagem.criado_por).thumbnail_home

        if postagem.criado_por not in perfis_postagens:
            perfis_postagens[postagem.criado_por] = PerfilModel.objects.get(usuario=postagem.criado_por)

        if postagem.pid not in qtd_comentarios:
            qtd = ComentarioGrupoModel.objects.filter(postagem=postagem, ativo=True)
            qtd_comentarios[postagem.pid] = len(qtd)

        if postagem.pid not in comentario_postagem:
            comentario_postagem[postagem.pid] = ComentarioGrupoModel.objects.filter(ativo=True, postagem=postagem)\
                .order_by('-data_criacao')

    for u_membro in membros:
        if u_membro.usuario not in usuarios:
            usuarios[u_membro.usuario] = ImagemModel.objects.get(perfil=u_membro.usuario.perfilmodel,
                                                                 is_profile_image=True)

    paginas = Paginator(postagens, 10)

    if request.method == 'GET':
        pagina = request.GET.get('pg')

        try:
            postagens = paginas.page(pagina)
        except PageNotAnInteger:
            postagens = paginas.page(1)
        except EmptyPage:
            postagens = paginas.page(paginas.num_pages)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'entrarGrupo' in request.POST:

            try:
                membro = MembroModel.objects.get(usuario=request.user, grupo=grupo)
                membro.ativo = True
            except MembroModel.DoesNotExist:
                membro = MembroModel()
                membro.grupo = grupo
                membro.usuario = request.user

            membro.save()

        if 'sairGrupo' in request.POST:
            membro.ativo = False
            membro.save()

        if 'criarPostagem' in request.POST:
            postagem_form = PostagemGrupoForm(data=request.POST)

            if postagem_form.is_valid():
                postagem = postagem_form.save(commit=False)

                postagem.titulo = postagem.titulo.capitalize()
                postagem.criado_por = request.user
                postagem.grupo = grupo
                postagem.data_criacao = timezone.now()
                postagem.save()

        if 'deleteComment' in request.POST:
            pcid = request.POST['deleteComment'].split('-')

            pid = int(pcid[0])
            cid = int(pcid[1])

            try:
                postagem = PostagemGrupoModel.objects.get(pid=pid)
                custom_query = Q(criado_por=request.user) | Q(postagem__criado_por=postagem.criado_por)

                comentario = ComentarioGrupoModel.objects.get(Q(postagem__pid=pid), Q(cid=cid), custom_query)

                comentario.ativo = False
                comentario.save()

            except ComentarioGrupoModel.DoesNotExist:
                pass

        if 'deletePost' in request.POST:
            pid = int(request.POST['deletePost'])

            try:
                postagem = PostagemGrupoModel.objects.get(pid=pid, criado_por=request.user)
                postagem.ativo = False
                postagem.save()

            except PostagemGrupoModel.DoesNotExist:
                pass

        if 'comentarPostagem' in request.POST:
            comentario_form = ComentarioGrupoForm(data=request.POST)

            if comentario_form.is_valid() and membro:
                comentario = comentario_form.save(commit=False)
                pid = request.POST.get('comentarPostagem')
                postagem = PostagemGrupoModel.objects.get(pid=pid)

                comentario.criado_por = request.user
                comentario.conteudo = request.POST['comentario']
                comentario.postagem = postagem
                comentario.data_criacao = timezone.now()
                comentario.save()

        return HttpResponseRedirect('/grupo/' + gid)
    else:
        comentario_form = ComentarioGrupoForm()
        postagem_form = PostagemGrupoForm()

    args['qtd_postagens'] = qtd_postagens
    args['interesses'] = interesses
    args['postagem_form'] = postagem_form
    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['qtd_comentarios'] = qtd_comentarios
    args['comentario_form'] = comentario_form
    args['postagens'] = postagens
    args['fotos_comentarios'] = fotos_comentarios
    args['fotos_postagens'] = fotos_postagens
    args['perfis_postagens'] = perfis_postagens
    args['perfis_comentarios'] = perfis_comentarios
    args['comentario_postagem'] = comentario_postagem
    args['membro'] = membro
    args['grupo'] = grupo
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)
    args['perfil'] = perfil
    args['foto'] = foto
    args['usuarios'] = usuarios

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
def view_sobre_grupo(request, gid):
    args = {}

    grupo = None

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        membro = MembroModel.objects.get(grupo=grupo, usuario=request.user, ativo=True)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        membro = None

    membros = MembroModel.objects.filter(grupo=grupo, ativo=True)
    interesses = GrupoInteresseModel.objects.filter(grupo=grupo)

    usuarios = {}

    for u_membro in membros:
        if u_membro.usuario not in usuarios:
            usuarios[u_membro.usuario] = ImagemModel.objects.get(perfil=u_membro.usuario.perfilmodel,
                                                                 is_profile_image=True)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'entrarGrupo' in request.POST:

            try:
                membro = MembroModel.objects.get(usuario=request.user, grupo=grupo)
                membro.ativo = True
            except MembroModel.DoesNotExist:
                membro = MembroModel()
                membro.grupo = grupo
                membro.usuario = request.user

            membro.save()

        if 'sairGrupo' in request.POST:
            membro.ativo = False
            membro.save()

        return HttpResponseRedirect('/grupo/' + gid + '/sobre/')

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['usuarios'] = usuarios
    args['interesses'] = interesses
    args['membro'] = membro
    args['grupo'] = grupo
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)
    args['perfil'] = perfil
    args['foto'] = foto

    return render(request, 'grupos/sobre_grupo.html', args)

@login_required
def view_lista_grupos(request):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    perfil_grupos = MembroModel.objects.filter(usuario=perfil.usuario, ativo=True)

    grupos = []

    if request.GET.get('gq'):
        grupo_search_form = GrupoSearchForm(data=request.GET)

        if grupo_search_form.is_valid():
            processed_data = ['xa2sipg39xlc4a6fop8rek5u7']
            query_data = grupo_search_form.cleaned_data.get('gq')
            args['data_list'] = query_data

            aspas = query_data.count('\"')

            if aspas > 0:
                if aspas % 2 == 0:
                    data_list = [data for data in query_data.split('\"') if data.strip()]
                else:
                    data_list = [query_data.replace('\"', '')]

            else:
                data_list = [query_data]

            for data in data_list:

                if data not in processed_data:

                    try:
                        query = GrupoModel.objects.filter(nome__icontains=data)
                        grupos = grupos + list(query)

                        if query:
                            processed_data.append(data)

                    except GrupoModel.DoesNotExist:
                        pass

            grupos = list(set(grupos))

            args['data'] = processed_data
    else:
        grupo_search_form = GrupoSearchForm()

    if request.method == 'POST':
        grupo_form = AdicionarGrupoForm()

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'criarGrupo' in request.POST:
            grupo_form = AdicionarGrupoForm(data=request.POST)

            if grupo_form.is_valid():
                grupo = grupo_form.save(commit=False)

                grupo_tmp = grupo_form.cleaned_data['criarGrupo']
                grupo_tmp = ' '.join(unicode(grupo_tmp).split())

                grupo.nome = grupo_tmp.title()
                grupo.criado_por = request.user
                grupo.descricao = 'Este grupo não possui uma descrição!'
                grupo.save()

                membro = MembroModel()
                membro.grupo = grupo
                membro.usuario = request.user
                membro.is_admin = True
                membro.save()

                return HttpResponseRedirect('/grupo/' + str(grupo.gid))

        if 'addGrupo' in request.POST:
            grupo_id = request.POST.get('addGrupo')
            grupo_obj = InteresseModel.objects.get(gid=grupo_id)

            membro = MembroModel()
            membro.grupo = grupo_obj
            membro.usuario = request.user
            membro.save()

            return HttpResponseRedirect('/grupo/lista/')

    else:
        grupo_form = AdicionarGrupoForm()

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['pesquisa_grupo_form'] = grupo_search_form
    args['grupo_form'] = grupo_form
    args['perfil_grupos'] = perfil_grupos
    args['grupos'] = grupos
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm()

    return render(request, 'grupos/lista_grupos.html', args)


@login_required
def view_pagina_interesse(request, iid):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    interesse = InteresseModel.objects.get(iid=iid, ativo=True)
    usuarios_interesse = UsuarioInteresseModel.objects.filter(interesse=interesse, ativo=True)
    grupos_interesse = GrupoInteresseModel.objects.filter(interesse=interesse, ativo=True)

    usuarios = {}

    for u_interesse in usuarios_interesse:
        if u_interesse.usuario not in usuarios:
            usuarios[u_interesse.usuario] = ImagemModel.objects.get(perfil=u_interesse.usuario.perfilmodel)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'adicionarInteresse' in request.POST:

            try:
                usuario_interesse = UsuarioInteresseModel.objects.get(interesse=interesse, usuario=request.user)
                usuario_interesse.ativo = True
            except UsuarioInteresseModel.DoesNotExist:
                usuario_interesse = UsuarioInteresseModel()
                usuario_interesse.usuario = request.user
                usuario_interesse.interesse = interesse

            usuario_interesse.save()

        if 'removerInteresse' in request.POST:
            usuario_interesse = UsuarioInteresseModel.objects.get(interesse=interesse, usuario=request.user)
            usuario_interesse.ativo = False
            usuario_interesse.save()

        return HttpResponseRedirect('/interesse/'+str(interesse.iid))

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['grupos_interesse'] = grupos_interesse
    args['usuarios_interesse'] = usuarios_interesse
    args['usuarios'] = usuarios
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
    perfil_interesses = UsuarioInteresseModel.objects.filter(usuario=perfil.usuario, ativo=True)

    interesses = []

    if request.GET.get('iq'):
        interesse_search_form = InteresseSearchForm(data=request.GET)

        if interesse_search_form.is_valid():
            processed_data = ['da2sipg34xlc4a5fop4rek5u2']
            query_data = interesse_search_form.cleaned_data.get('iq')
            args['data_list'] = query_data

            aspas = query_data.count('\"')

            if aspas > 0:
                if aspas % 2 == 0:
                    data_list = [data for data in query_data.split('\"') if data.strip()]
                else:
                    data_list = [query_data.replace('\"', '')]

            else:
                data_list = [query_data]

            for data in data_list:

                if data not in processed_data:

                    try:
                        query = InteresseModel.objects.filter(interesse__icontains=data, ativo=True)
                        interesses = interesses + list(query)

                        if query:
                            processed_data.append(data)

                    except InteresseModel.DoesNotExist:
                        pass

            interesses = list(set(interesses))

            args['data'] = processed_data
    else:
        interesse_search_form = InteresseSearchForm()

    if request.method == 'POST':
        interesse_form = AdicionarInteresseForm()

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'criarInteresse' in request.POST:
            interesse_form = AdicionarInteresseForm(data=request.POST)

            if interesse_form.is_valid():
                interesse = interesse_form.save(commit=False)

                interesse_tmp = interesse_form.cleaned_data['criarInteresse']
                interesse_tmp = ' '.join(unicode(interesse_tmp).split())

                interesse.interesse = interesse_tmp.title()
                interesse.criado_por = request.user
                interesse.save()

                usuario_interesse = UsuarioInteresseModel()
                usuario_interesse.interesse = interesse
                usuario_interesse.usuario = request.user
                usuario_interesse.save()

                return HttpResponseRedirect('/interesse/lista/')

        if 'addInteresse' in request.POST:
            interesse_id = request.POST.get('addInteresse')
            interesse_obj = InteresseModel.objects.get(iid=interesse_id)

            usuario_interesse = UsuarioInteresseModel()
            usuario_interesse.interesse = interesse_obj
            usuario_interesse.usuario = request.user
            usuario_interesse.save()

            return HttpResponseRedirect('/interesse/lista/')

    else:
        interesse_form = AdicionarInteresseForm()

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['pesquisa_interesse_form'] = interesse_search_form
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
        MembroModel.objects.get(grupo=grupo, usuario=request.user, ativo=True)

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
        pagina = request.GET.get('pg')

        try:
            comentarios = paginas.page(pagina)
        except PageNotAnInteger:
            comentarios = paginas.page(1)
        except EmptyPage:
            comentarios = paginas.page(paginas.num_pages)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

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

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
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


@login_required
def view_lista_eventos(request, gid):
    args = {}

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        membro = MembroModel.objects.get(usuario=request.user, ativo=True, grupo=grupo)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        return HttpResponseRedirect('/grupo/' + gid)

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)

    membros = MembroModel.objects.filter(grupo=grupo, ativo=True)
    eventos = EventoModel.objects.filter(grupo=grupo, ativo=True).order_by('data_evento')

    paginas = Paginator(eventos, 10)
    participando_dict = {}

    if request.method == 'GET':
        pagina = request.GET.get('pg')

        try:
            eventos = paginas.page(pagina)
        except PageNotAnInteger:
            eventos = paginas.page(1)
        except EmptyPage:
            eventos = paginas.page(paginas.num_pages)

    for evento in eventos:

        if request.user not in participando_dict:
            try:
                ParticipaEventoModel.objects.get(evento=evento, ativo=True, usuario=request.user)
                participando_dict[evento] = True

            except ParticipaEventoModel.DoesNotExist:
                participando_dict[evento] = False

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'participarEvento' in request.POST:
            eid = request.POST.get('participarEvento')
            evento = EventoModel.objects.get(eid=eid)

            print eid

            try:
                participa = ParticipaEventoModel.objects.get(evento=evento, usuario=request.user)
                participa.ativo = True
            except ParticipaEventoModel.DoesNotExist:
                participa = ParticipaEventoModel()
                participa.evento = evento
                participa.usuario = request.user

            participa.save()

        if 'sairEvento' in request.POST:
            eid = request.POST.get('sairEvento')
            evento = EventoModel.objects.get(eid=eid)

            try:
                participa = ParticipaEventoModel.objects.get(evento=evento, usuario=request.user)
                participa.ativo = False
                participa.save()
            except ParticipaEventoModel.DoesNotExist:
                pass

        return HttpResponseRedirect('')

    args['participando'] = participando_dict
    args['membro'] = membro
    args['qtd_membros'] = len(list(membros))
    args['qtd_eventos'] = len(list(eventos))
    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['perfil'] = perfil
    args['foto'] = foto
    args['grupo'] = grupo
    args['eventos'] = eventos
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    return render(request, 'grupos/lista_eventos.html', args)


@login_required
def view_evento_grupo(request, gid, eid):
    args = {}

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        membro = MembroModel.objects.get(usuario=request.user, ativo=True, grupo=grupo)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        return HttpResponseRedirect('/grupo/' + gid)

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True, is_active=True)

    evento = EventoModel.objects.get(eid=eid, ativo=True)
    postagens = PostagemEventoModel.objects.filter(evento=evento, grupo=grupo, ativo=True)
    comentarios = ComentarioEventoModel.objects.filter(postagem__in=postagens, ativo=True)
    participando = ParticipaEventoModel.objects.filter(evento=evento, ativo=True)

    participantes = {}
    comentario_postagem = {}
    fotos_comentarios = {}
    fotos_postagens = {}
    perfis_comentarios = {}
    perfis_postagens = {}
    qtd_comentarios = {}

    for comentario in comentarios:
        if comentario.criado_por not in fotos_comentarios:
            fotos_comentarios[comentario.criado_por] = \
                ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                        perfil__usuario=comentario.criado_por).thumbnail

        if comentario.criado_por not in perfis_comentarios:
            perfis_comentarios[comentario.criado_por] = PerfilModel.objects.get(usuario=comentario.criado_por)

    for postagem in postagens:
        if postagem.criado_por not in fotos_postagens:
            fotos_postagens[postagem.criado_por] = \
                ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                        perfil__usuario=postagem.criado_por).thumbnail_home

        if postagem.criado_por not in perfis_postagens:
            perfis_postagens[postagem.criado_por] = PerfilModel.objects.get(usuario=postagem.criado_por)

        if postagem.pid not in qtd_comentarios:
            qtd = ComentarioEventoModel.objects.filter(postagem=postagem, ativo=True)
            qtd_comentarios[postagem.pid] = len(qtd)

        if postagem.pid not in comentario_postagem:
            comentario_postagem[postagem.pid] = ComentarioEventoModel.objects.filter(ativo=True, postagem=postagem)\
                .order_by('-data_criacao')

    paginas = Paginator(postagens, 10)

    if request.method == 'GET':
        pagina = request.GET.get('pg')

        try:
            postagens = paginas.page(pagina)
        except PageNotAnInteger:
            postagens = paginas.page(1)
        except EmptyPage:
            postagens = paginas.page(paginas.num_pages)

    for participante in participando:
        if participante.usuario not in participando:
            participantes[participante.usuario] = ImagemModel.objects.get(perfil=participante.usuario.perfilmodel,
                                                                          is_profile_image=True, is_active=True)

    try:
        participa = ParticipaEventoModel.objects.get(usuario=request.user, evento=evento, ativo=True)

    except ParticipaEventoModel.DoesNotExist:
        participa = None

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'participarEvento' in request.POST:
            eid = request.POST.get('participarEvento')
            evento = EventoModel.objects.get(eid=eid)

            try:
                participa = ParticipaEventoModel.objects.get(evento=evento, usuario=request.user)
                participa.ativo = True
            except ParticipaEventoModel.DoesNotExist:
                participa = ParticipaEventoModel()
                participa.evento = evento
                participa.usuario = request.user

            participa.save()

        if 'sairEvento' in request.POST:
            eid = request.POST.get('sairEvento')
            evento = EventoModel.objects.get(eid=eid)

            try:
                participa = ParticipaEventoModel.objects.get(evento=evento, usuario=request.user)
                participa.ativo = False
                participa.save()
            except ParticipaEventoModel.DoesNotExist:
                pass

        if 'criarPostagem' in request.POST:
            postagem_form = PostagemEventoForm(data=request.POST)

            if postagem_form.is_valid():
                postagem = postagem_form.save(commit=False)

                postagem.titulo = postagem.titulo.capitalize()
                postagem.criado_por = request.user
                postagem.evento = evento
                postagem.grupo = grupo
                postagem.data_criacao = timezone.now()
                postagem.save()

        if 'deleteComment' in request.POST:
            pcid = request.POST['deleteComment'].split('-')

            pid = int(pcid[0])
            cid = int(pcid[1])

            try:
                postagem = PostagemEventoModel.objects.get(pid=pid)
                custom_query = Q(criado_por=request.user) | Q(postagem__criado_por=postagem.criado_por)

                comentario = ComentarioEventoModel.objects.get(Q(postagem__pid=pid), Q(cid=cid), custom_query)

                comentario.ativo = False
                comentario.save()

            except ComentarioEventoModel.DoesNotExist:
                pass

        if 'deletePost' in request.POST:
            pid = int(request.POST['deletePost'])

            try:
                postagem = PostagemEventoModel.objects.get(pid=pid, criado_por=request.user)
                postagem.ativo = False
                postagem.save()

            except PostagemEventoModel.DoesNotExist:
                pass

        if 'comentarPostagem' in request.POST:
            comentario_form = ComentarioEventoForm(data=request.POST)

            if comentario_form.is_valid() and membro:
                comentario = comentario_form.save(commit=False)
                pid = request.POST.get('comentarPostagem')
                postagem = PostagemEventoModel.objects.get(pid=pid)

                comentario.criado_por = request.user
                comentario.conteudo = request.POST['comentario']
                comentario.postagem = postagem
                comentario.data_criacao = timezone.now()
                comentario.save()

        return HttpResponseRedirect('')
    else:
        postagem_form = PostagemEventoForm()

    args['qtd_comentarios'] = qtd_comentarios
    args['fotos_comentarios'] = fotos_comentarios
    args['fotos_postagens'] = fotos_postagens
    args['perfis_postagens'] = perfis_postagens
    args['perfis_comentarios'] = perfis_comentarios
    args['comentario_postagem'] = comentario_postagem
    args['postagem_form'] = postagem_form
    args['participantes'] = participantes
    args['membro'] = membro
    args['qtd_participando'] = len(list(participando))
    args['qtd_postagens'] = len(list(postagens))
    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['participa'] = participa
    args['postagens'] = postagens
    args['comentarios'] = comentarios
    args['evento'] = evento
    args['perfil'] = perfil
    args['foto'] = foto
    args['grupo'] = grupo
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    return render(request, 'grupos/evento.html', args)


@login_required
def view_postagem_evento(request, gid, eid, pid):
    args = {}

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        MembroModel.objects.get(grupo=grupo, usuario=request.user, ativo=True)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        return HttpResponseRedirect('/grupo/' + gid + '/')

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    postagem = get_object_or_404(PostagemEventoModel, grupo__gid=gid, pid=pid, ativo=True)
    comentarios = ComentarioEventoModel.objects.filter(postagem=postagem,
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
        pagina = request.GET.get('pg')

        try:
            comentarios = paginas.page(pagina)
        except PageNotAnInteger:
            comentarios = paginas.page(1)
        except EmptyPage:
            comentarios = paginas.page(paginas.num_pages)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'deleteComment' in request.POST:
            cid = int(request.POST['deleteComment'])

            try:
                custom_query = Q(criado_por=request.user) | Q(criado_por=postagem.criado_por)
                comentario = ComentarioEventoModel.objects.get(Q(postagem__pid=pid), Q(cid=cid), custom_query)
                comentario.ativo = False
                comentario.save()

            except ComentarioGrupoModel.DoesNotExist:
                pass

        if 'deletePost' in request.POST:

            try:
                postagem.ativo = False
                postagem.save()

                return HttpResponseRedirect('/grupo/' + gid + '/evento/' + eid)

            except PostagemEventoModel.DoesNotExist:
                pass

        if 'comment' in request.POST:
            comentario_form = ComentarioEventoForm(data=request.POST)

            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)

                comentario.criado_por = request.user
                comentario.conteudo = request.POST['comentario']
                comentario.postagem = postagem
                comentario.data_criacao = timezone.now()
                comentario.save()

        return HttpResponseRedirect('/grupo/' + gid + '/evento/' + eid + '/post/' + pid)

    else:
        comentario_form = ComentarioGrupoForm()

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
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

    return render(request, 'grupos/postagem_evento.html', args)


@login_required
def view_convites(request):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True, is_active=True)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_amigos_post(request, 'conviteAmigoFormPg')
        convites_grupos_post(request, 'conviteGrupoForm')
        convites_grupos_post(request, 'conviteGrupoFormPg')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_eventos_post(request, 'conviteEventoFormPg')

        return HttpResponseRedirect('/convites/')

    convites_grupos = load_convites_grupos(request)
    convites_eventos = load_convites_eventos(request)
    convites_amigos = load_convites_amigos(perfil)

    qtd_convites = len(convites_grupos) + len(convites_eventos) + len(convites_amigos)

    args['qtd_convites'] = qtd_convites
    args['convites_grupos'] = convites_grupos
    args['convites_eventos'] = convites_eventos
    args['convites_amigos'] = convites_amigos
    args['perfil'] = perfil
    args['foto'] = foto
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    return render(request, 'grupos/convites.html', args)


@login_required
def view_grupo_interesses(request, gid):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    grupo = GrupoModel.objects.get(gid=gid)
    grupo_interesses = GrupoInteresseModel.objects.filter(grupo=grupo, ativo=True)

    interesses = []

    if request.GET.get('iq'):
        interesse_search_form = InteresseSearchForm(data=request.GET)

        if interesse_search_form.is_valid():
            processed_data = ['da2sipg34xlc4a5fop4rek5u2']
            query_data = interesse_search_form.cleaned_data.get('iq')
            args['data_list'] = query_data

            aspas = query_data.count('\"')

            if aspas > 0:
                if aspas % 2 == 0:
                    data_list = [data for data in query_data.split('\"') if data.strip()]
                else:
                    data_list = [query_data.replace('\"', '')]

            else:
                data_list = [query_data]

            for data in data_list:

                if data not in processed_data:

                    try:
                        query = InteresseModel.objects.filter(interesse__icontains=data, ativo=True)
                        interesses = interesses + list(query)

                        if query:
                            processed_data.append(data)

                    except InteresseModel.DoesNotExist:
                        pass

            interesses = list(set(interesses))

            args['data'] = processed_data
    else:
        interesse_search_form = InteresseSearchForm()

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'criarInteresse' in request.POST:
            interesse_form = AdicionarInteresseForm(data=request.POST)

            if interesse_form.is_valid():
                interesse = interesse_form.save(commit=False)

                interesse_tmp = interesse_form.cleaned_data['criarInteresse']
                interesse_tmp = ' '.join(unicode(interesse_tmp).split())

                interesse.interesse = interesse_tmp.title()
                interesse.criado_por = request.user
                interesse.save()

                usuario_interesse = UsuarioInteresseModel()
                usuario_interesse.interesse = interesse
                usuario_interesse.usuario = request.user
                usuario_interesse.save()

                grupo_interesse = GrupoInteresseModel()
                grupo_interesse.interesse = interesse
                grupo_interesse.grupo = grupo
                grupo_interesse.save()

        if 'addInteresse' in request.POST:
            interesse_id = request.POST.get('addInteresse')
            interesse_obj = InteresseModel.objects.get(iid=interesse_id, ativo=True)

            try:
                grupo_interesse = GrupoInteresseModel.objects.get(grupo=grupo, interesse=interesse_obj)
                grupo_interesse.ativo = True

            except GrupoInteresseModel.DoesNotExist:
                grupo_interesse = GrupoInteresseModel()
                grupo_interesse.interesse = interesse_obj
                grupo_interesse.grupo = grupo

            grupo_interesse.save()

        if 'delInteresse' in request.POST:
            interesse_id = request.POST.get('delInteresse')
            interesse_obj = InteresseModel.objects.get(iid=interesse_id, ativo=True)

            grupo_interesse = GrupoInteresseModel.objects.get(grupo=grupo, interesse=interesse_obj)
            grupo_interesse.ativo = False
            grupo_interesse.save()

        return HttpResponseRedirect('/grupo/' + gid + '/interesses/')

    else:
        interesse_form = AdicionarInteresseForm()

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['pesquisa_interesse_form'] = interesse_search_form
    args['interesse_form'] = interesse_form
    args['grupo_interesses'] = grupo_interesses
    args['grupo'] = grupo
    args['interesses'] = interesses
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm()

    return render(request, 'grupos/interesses_grupo.html', args)


@login_required
def view_grupo_convidar(request, gid):
    args = {}

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        MembroModel.objects.get(grupo=grupo, usuario=request.user, ativo=True)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        return HttpResponseRedirect('/grupo/' + gid + '/')

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    usuario_amigos = AmigoModel.objects.filter(perfil=request.user.perfilmodel, ativo=True)
    membros = MembroModel.objects.filter(grupo=grupo)
    convidados = ConviteGrupoModel.objects.filter(grupo=grupo, ativo=True)

    convidados_dict = {}
    amigos_dict = {}
    usuarios_dict = {}

    membros_list = []
    usuarios = []

    if request.GET.get('aq'):
        usuario_search_form = MembroSearchForm(data=request.GET)

        if usuario_search_form.is_valid():
            processed_data = ['da2sipg34xlc4a5fop4rek5u2']
            query_data = usuario_search_form.cleaned_data.get('aq')
            args['data_list'] = query_data

            aspas = query_data.count('\"')

            if aspas > 0:
                if aspas % 2 == 0:
                    data_list = [data for data in query_data.split('\"') if data.strip()]
                else:
                    data_list = [query_data.replace('\"', '')]

            else:
                data_list = [query_data]

            for data in data_list:

                if data not in processed_data:

                    try:
                        query = UsuarioModel.object.filter(full_name__icontains=data, is_active=True)
                        usuarios = usuarios + list(query)

                        if query:
                            processed_data.append(data)

                    except AmigoModel.DoesNotExist:
                        pass

            usuarios = list(set(usuarios))

            args['data'] = processed_data
    else:
        usuario_search_form = MembroSearchForm()

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'cancelUsuario' in request.POST:
            uid = request.POST.get('cancelUsuario')
            usuario_obj = UsuarioModel.object.get(uid=uid)

            try:
                convite = ConviteGrupoModel.objects.get(convidado=usuario_obj, grupo=grupo)
                convite.ativo = False
                convite.save()

            except ConviteGrupoModel.DoesNotExist:
                pass

        if 'inviteUsuario' in request.POST:
            uid = request.POST.get('inviteUsuario')
            usuario_obj = UsuarioModel.object.get(uid=uid)

            try:
                convite = ConviteGrupoModel.objects.get(convidado=usuario_obj, grupo=grupo)
                convite.ativo = True

            except ConviteGrupoModel.DoesNotExist:
                convite = ConviteGrupoModel()
                convite.usuario = request.user
                convite.convidado = usuario_obj
                convite.grupo = grupo

            convite.save()

        return HttpResponseRedirect('/grupo/' + gid + '/convidar/')

    for amigo in usuario_amigos:
        amigos_dict[amigo] = ImagemModel.objects.get(perfil=amigo.amigo, is_profile_image=True)

    for usuario in usuarios:
        if usuario not in usuarios_dict:
            usuarios_dict[usuario] = ImagemModel.objects.get(perfil=usuario.perfilmodel, is_profile_image=True)

    for membro in membros:
        if membro not in membros_list:
            membros_list.append(membro.usuario)

    for convite in convidados:
        if convite not in convidados_dict:
            convidados_dict[convite.convidado] = ImagemModel.objects.get(perfil=convite.convidado.perfilmodel,
                                                                         is_profile_image=True)

    args['convidados'] = convidados
    args['list_convidados'] = convidados_dict
    args['membros'] = membros_list
    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['pesquisa_usuario_form'] = usuario_search_form
    args['usuario_amigos'] = amigos_dict
    args['grupo'] = grupo
    args['usuarios'] = usuarios_dict
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm()

    return render(request, 'grupos/convidar.html', args)


@login_required
def view_evento_convidar(request, gid, eid):
    args = {}

    try:
        grupo = GrupoModel.objects.get(gid=gid)
        MembroModel.objects.get(grupo=grupo, usuario=request.user, ativo=True)

    except GrupoModel.DoesNotExist:
        return HttpResponseRedirect('/')

    except MembroModel.DoesNotExist:
        return HttpResponseRedirect('/grupo/' + gid + '/')

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    grupo = GrupoModel.objects.get(gid=gid)
    membros = MembroModel.objects.filter(grupo=grupo)
    evento = EventoModel.objects.get(eid=eid)
    convidados = ConviteEventoModel.objects.filter(evento=evento, ativo=True)
    participa = ParticipaEventoModel.objects.filter(evento=evento, ativo=True)

    convidados_dict = {}
    membros_dict = {}

    participa_list = []

    for participante in participa:
        participa_list.append(participante.usuario)

    if request.method == 'POST':
        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'inviteAll' in request.POST:

            for membro in membros:
                if membro.usuario not in participa_list:

                    try:
                        convite = ConviteEventoModel.objects.get(convidado=membro.usuario, evento=evento)
                        convite.ativo = True

                    except ConviteEventoModel.DoesNotExist:
                        convite = ConviteEventoModel()
                        convite.usuario = request.user
                        convite.convidado = membro.usuario
                        convite.evento = evento
                        convite.grupo = grupo

                    convite.save()

        if 'cancelUsuario' in request.POST:
            uid = request.POST.get('cancelUsuario')
            usuario_obj = UsuarioModel.object.get(uid=uid)

            try:
                convite = ConviteEventoModel.objects.get(convidado=usuario_obj, evento=evento)
                convite.ativo = False
                convite.save()

            except ConviteEventoModel.DoesNotExist:
                pass

        if 'inviteUsuario' in request.POST:
            uid = request.POST.get('inviteUsuario')
            usuario_obj = UsuarioModel.object.get(uid=uid)

            try:
                convite = ConviteEventoModel.objects.get(convidado=usuario_obj, evento=evento)
                convite.ativo = True

            except ConviteEventoModel.DoesNotExist:
                convite = ConviteEventoModel()
                convite.usuario = request.user
                convite.convidado = usuario_obj
                convite.evento = evento
                convite.grupo = grupo

            convite.save()

        return HttpResponseRedirect('/grupo/' + gid + '/evento/' + eid + '/convidar/')

    for membro in membros:
        if membro not in membros_dict:
            membros_dict[membro.usuario] = ImagemModel.objects.get(perfil=membro.usuario.perfilmodel,
                                                                   is_profile_image=True)

    for convite in convidados:
        if convite not in convidados_dict:
            convidados_dict[convite.convidado] = ImagemModel.objects.get(perfil=convite.convidado.perfilmodel,
                                                                         is_profile_image=True)

    args['participante'] = participa_list
    args['convidados'] = convidados
    args['list_convidados'] = convidados_dict
    args['membros'] = membros_dict
    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['grupo'] = grupo
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm()

    return render(request, 'grupos/convidar_evento.html', args)