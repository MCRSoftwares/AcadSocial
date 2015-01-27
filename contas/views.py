# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v009a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002, RF013, RF019, RF020, RF021, RF022, RF023, RF027
Caso(s) de Uso: DV001, DV002, DVA010, DVA012, PD005

Descrição:
    Definição das views relacionadas à aplicação de contas (cadastro/login).
"""

# TODO Configurar views que possuem notificações

from contas.forms import UsuarioCadastroForm, PerfilCadastroForm, UsuarioLoginForm, PerfilEditForm, UsuarioEditForm
from contas.forms import EnviarTokenForm, SenhaResetForm
from universidades.models import UniversidadeModel
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout
from datetime import datetime, timedelta
from django.utils import timezone
from contas.models import PerfilModel, UsuarioModel, TokenModel
from contas.methods import gerar_token, enviar_email_ativacao, calcular_idade, login_form_body
from contas.methods import redirecionar_para, enviar_email_senha_reset, calcular_aniversario
from django.contrib.auth.decorators import login_required
from contas.constants import TOKEN_TYPE
from mainAcad.forms import UsuarioSearchForm, ImagemUploadForm
from mainAcad.models import ImagemModel, AmigoModel, ConviteAmigoModel
from grupos.models import UsuarioInteresseModel, MembroModel, PostagemGrupoModel, ComentarioGrupoModel, GrupoModel
from grupos.methods import load_convites_grupos, load_convites_amigos, load_convites_eventos
from grupos.methods import convites_amigos_post, convites_grupos_post, convites_eventos_post
from grupos.forms import ComentarioGrupoForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse


def view_cadastrar_usuario(request):
    args = {}

    # Se o usuário já estiver logado, ele será redirecionado para a página inicial

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST' and 'loginForm' in request.POST:
        login_form = UsuarioLoginForm(data=request.POST)

        return login_form_body(request, view_login_usuario, login_form, login)
    else:
        login_form = UsuarioLoginForm()

    if request.method == 'POST' and 'cadastroForm' in request.POST:
        usuario_form = UsuarioCadastroForm(data=request.POST)
        perfil_form = PerfilCadastroForm(data=request.POST)
        foto_form = ImagemUploadForm(files=request.FILES)

        if usuario_form.is_valid() and perfil_form.is_valid() and foto_form.is_valid():

            # Passando as informações do formuário para seus respectivos modelos.

            usuario = usuario_form.save()
            usuario.email = usuario_form.cleaned_data['email'].lower()
            usuario.set_password(usuario.password)
            usuario.save()

            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario

            # Geração da chave de ativação do usuário.

            email = usuario.email
            nome = usuario_form.cleaned_data['first_name']
            sobrenome = usuario_form.cleaned_data['last_name']

            token = TokenModel()

            # Método que preenche os atributos de TokenModel

            token = gerar_token(TOKEN_TYPE[0], usuario, token, email, timezone.now() + timedelta(days=7))

            # Formatação da data de nascimento do usuário

            dia = perfil_form.cleaned_data['dia']
            mes = perfil_form.cleaned_data['mes']
            ano = perfil_form.cleaned_data['ano']

            data_str = '%s-%s-%s' % (dia, mes, ano)
            perfil.data_nascimento = datetime.strptime(data_str, '%d-%m-%Y')

            # Finalização das configurações do perfil de usuário -> perfil salvo

            perfil.save()

            # Fazendo upload da foto

            foto = foto_form.save(commit=False)
            foto.perfil = perfil
            foto.is_profile_image = True

            foto.save()

            # Enviando e-mail de validação da conta para o usuário

            enviar_email_ativacao(email, nome, sobrenome, token.token)

            args['usuario'] = usuario
            args['login_form'] = login_form
            args['token'] = token

            return render(request, 'contas/cadastro_sucesso.html', args)
    else:
        usuario_form = UsuarioCadastroForm()
        perfil_form = PerfilCadastroForm()
        foto_form = ImagemUploadForm()

        args['usuario'] = None

    args['usuario_form'] = usuario_form
    args['perfil_form'] = perfil_form
    args['foto_form'] = foto_form
    args['login_form'] = login_form

    return render(request, 'contas/cadastro.html', args)


def view_pagina_inicial(request):

    # Checa se o usuário já está logado

    if not request.user.is_authenticated():
        return view_pagina_inicial_login(request)

    return view_pagina_inicial_logada(request)


def view_pagina_inicial_login(request):
    args = {}

    # Checa se o usuário já está logado.

    if request.user.is_authenticated():
        return view_pagina_inicial_logada(request)

    if request.method == 'POST':
        login_form = UsuarioLoginForm(data=request.POST)

        # Caso o login ocorra de forma correta (campos corretos).

        if login_form.is_valid():
            login(request, login_form.get_usuario())

            # Se o usuário for um superuser, este será redirecionado para a página de admin.

            if request.user.is_superuser:
                return HttpResponseRedirect('/admin')

            # Se for um usuário normal, ele será mandado para a view da página principal.

            return HttpResponseRedirect(reverse('index', args=[]))
        else:
            return view_login_usuario(request)
    else:
        login_form = UsuarioLoginForm(request)

    args['login_form'] = login_form

    return render(request, 'contas/index.html', args)


def view_pagina_inicial_logada(request):
    args = {}

    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin', args=[]))

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True, is_active=True)

    interesses = UsuarioInteresseModel.objects.filter(usuario=request.user, ativo=True).order_by('-data_criacao')
    grupos_participa = MembroModel.objects.filter(usuario=request.user, ativo=True).order_by('-data_entrada')
    grupos = GrupoModel.objects.filter(membromodel__in=grupos_participa, ativo=True)
    postagens = PostagemGrupoModel.objects.filter(grupo__in=grupos, ativo=True).order_by('-data_criacao')
    comentarios = ComentarioGrupoModel.objects.filter(postagem__in=postagens, ativo=True)

    comentario_postagem = {}
    fotos_comentarios = {}
    fotos_postagens = {}
    perfis_comentarios = {}
    perfis_postagens = {}
    qtd_comentarios = {}

    paginas = Paginator(postagens, 10)

    if request.method == 'GET':
        pagina = request.GET.get('pg')

        try:
            postagens = paginas.page(pagina)
        except PageNotAnInteger:
            postagens = paginas.page(1)
        except EmptyPage:
            postagens = paginas.page(paginas.num_pages)

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

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

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
            pid = request.POST.get('comentarPostagem')
            postagem = PostagemGrupoModel.objects.get(pid=pid)

            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)

                comentario.criado_por = request.user
                comentario.conteudo = request.POST['comentario']
                comentario.postagem = postagem
                comentario.data_criacao = timezone.now()
                comentario.save()

        return HttpResponseRedirect('/')
    else:
        comentario_form = ComentarioGrupoForm()

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['qtd_comentarios'] = qtd_comentarios
    args['comentario_form'] = comentario_form
    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(request.GET)
    args['interesses_possui'] = interesses
    args['grupos_participa'] = grupos_participa
    args['postagens'] = postagens
    args['fotos_comentarios'] = fotos_comentarios
    args['fotos_postagens'] = fotos_postagens
    args['perfis_postagens'] = perfis_postagens
    args['perfis_comentarios'] = perfis_comentarios
    args['comentario_postagem'] = comentario_postagem

    return render(request, 'contas/home.html', args)


def view_login_usuario(request):
    args = {}

    # Checa se o usuário já está logado.

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST' and 'loginForm' in request.POST:
        login_form = UsuarioLoginForm(data=request.POST)

        # Caso o login ocorra de forma correta (campos corretos).

        if login_form.is_valid():
            login(request, login_form.get_usuario())

            # Se o usuário for um superuser, este será redirecionado para a página de admin.

            if request.user.is_superuser:
                return HttpResponseRedirect('/admin')

            # Se for um usuário normal, ele será mandado para a view da página principal.

            return redirect(redirecionar_para(request.get_full_path()))

    else:
        login_form = UsuarioLoginForm(request)

    args['login_form'] = login_form

    return render(request, 'contas/login.html', args)


def view_logout_usuario(request):
    logout(request)

    return HttpResponseRedirect('/')


def view_confirmar_usuario(request, chave):
    args = {}

    if request.method == 'POST' and 'loginForm' in request.POST:
        login_form = UsuarioLoginForm(data=request.POST)
        return login_form_body(request, view_login_usuario, login_form, login)
    else:
        login_form = UsuarioLoginForm()

    args['login_form'] = login_form

    if request.user.is_authenticated():
        # Se o usuário já estiver logado, ele será redirecionado para a página inicial.
        return HttpResponseRedirect('/')

    # Confere se existe algum perfil que possui a chave dada. Caso não exista, o sistema retorna 404.

    token = get_object_or_404(TokenModel, token=chave, valid=True)

    # Checa se o token expirou (no caso de confirmação de usuário, o tempo de vida do token é de 7 dias).

    if token.data_expiracao < timezone.now():
        token.active = False
        token.save()

    # Se o token estiver ativo (ou seja, não expirou), o usuário será ativado.

    if token.active:
        usuario = token.usuario
        usuario.is_active = True
        usuario.save()
        args['usuario'] = usuario

        # O token é definido como inválido, para que não possa ser acessado novamente.

        token.valid = False
        token.save()

    # Se o token expirou, o usuário verá o formulário de reenvio do e-mail de ativação.

    if request.method == 'POST':
        ativacao_form = EnviarTokenForm(data=request.POST)

        if ativacao_form.is_valid():
            email = ativacao_form.cleaned_data['email']
            usuario = UsuarioModel.object.get(email=email)

            # Gera um novo token de ativação de conta para o usuário

            novo_token = TokenModel()
            novo_token = gerar_token(TOKEN_TYPE[0], usuario, novo_token, email,  timezone.now() + timedelta(days=7))

            # Envia um novo e-mail de ativação para o usuário

            enviar_email_ativacao(email, usuario.first_name, usuario.last_name, novo_token.token)

            args['email'] = email

            # O token anterior passa a ser inválido, para que não possa ser acessado novamente.

            token.valid = False
            token.save()

            args['usuario'] = usuario

            return render(request, 'contas/cadastro_email_ativacao.html', args)
    else:
        ativacao_form = EnviarTokenForm()

        # Define o valor do campo 'email' para o e-mail do usuário que acessou a página.

        ativacao_form.fields['email'].widget.attrs['value'] = token.usuario.email

    args['expired'] = not token.active
    args['ativacao_form'] = ativacao_form
    args['token'] = token

    return render(request, 'contas/cadastro_confirmar.html', args)


def view_senha_reset(request):
    args = {}

    if request.method == 'POST' and 'loginForm' in request.POST:
        login_form = UsuarioLoginForm(data=request.POST)
        return login_form_body(request, view_login_usuario, login_form, login)
    else:
        login_form = UsuarioLoginForm()

    if request.method == 'POST':
        senha_form = EnviarTokenForm(data=request.POST)

        if senha_form.is_valid():

            # Resgata as informações do usuário que requisitou a redefinição de senha.

            email = senha_form.cleaned_data['email']
            usuario = UsuarioModel.object.get(email=email)
            args['user_email'] = email
            # Gera um token de redefinição de senha.

            token = TokenModel()
            token = gerar_token(TOKEN_TYPE[1], usuario, token, email)
            enviar_email_senha_reset(token, usuario, email)

            return render(request, 'contas/senha_reset_completo.html', args)
    else:
        senha_form = EnviarTokenForm()

    args['senha_form'] = senha_form
    args['login_form'] = login_form

    return render(request, 'contas/senha_reset.html', args)


def view_senha_reset_confirmado(request, uid, chave):
    args = {}

    if request.method == 'POST' and 'loginForm' in request.POST:
        login_form = UsuarioLoginForm(data=request.POST)
        return login_form_body(request, view_login_usuario, login_form, login)
    else:
        login_form = UsuarioLoginForm()

    # Procura por um token que possua a chave dada e seja válido.

    token = get_object_or_404(TokenModel, token=chave, valid=True)

    # Procura pelo usuário que possui o ID dado.

    usuario = get_object_or_404(UsuarioModel, uid=uid)

    # Checa se o token está ativo (ou seja, se ele não expirou).

    if token.data_expiracao < timezone.now():
        token.active = False
        token.save()

    if request.method == 'POST':
        senha_form = SenhaResetForm(data=request.POST)

        if senha_form.is_valid():

            # Redefine a senha do usuário.

            senha = senha_form.cleaned_data['senha']

            usuario.set_password(senha)
            usuario.save()

            # Define o token como inválido, para que não possa ser acessado novamente.

            token.valid = False
            token.save()

            args['login_form'] = login_form

            return render(request, 'contas/senha_reset_finalizado.html', args)

    else:
        senha_form = SenhaResetForm()

    args['expired'] = not token.active
    args['senha_form'] = senha_form
    args['login_form'] = login_form
    args['token'] = token

    return render(request, 'contas/senha_reset_confirmado.html', args)


def view_reativar_usuario(request):
    args = {}

    if request.method == 'POST' and 'loginForm' in request.POST:
        login_form = UsuarioLoginForm(data=request.POST)
        return login_form_body(request, view_login_usuario, login_form, login)
    else:
        login_form = UsuarioLoginForm()

    args['login_form'] = login_form

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        reativar_form = EnviarTokenForm(data=request.POST)

        if reativar_form.is_valid():
            email = reativar_form.cleaned_data['email'].lower()
            usuario = UsuarioModel.object.get(email=email)

            # Checa se o usuário desativado possui algum token ativo

            tokens_ativados = TokenModel.objects.filter(usuario=usuario, active=True, valid=True)

            # Define todos os tokens ativos e validos como inativos (expirados) e como inválidos.

            for token in tokens_ativados:
                token.active = False
                token.valid = False
                token.save()

            # Gera um novo token de ativação de conta para o usuário

            novo_token = TokenModel()
            novo_token = gerar_token(TOKEN_TYPE[0], usuario, novo_token, email, timezone.now() + timedelta(days=7))

            # Envia um novo e-mail de ativação para o usuário

            enviar_email_ativacao(email, usuario.first_name, usuario.last_name, novo_token.token)

            args['finalizado'] = True
            args['usuario'] = usuario
    else:
        reativar_form = EnviarTokenForm()
        args['finalizado'] = False

    args['reativar_form'] = reativar_form

    return render(request, 'contas/cadastro_reativar.html', args)


@login_required
def view_perfil_usuario(request, sigla, perfil_link):
    args = {}

    # Procura por um usuário e perfil existente que pertença ao link dado.

    universidade = get_object_or_404(UniversidadeModel, sigla_campus=sigla)
    pag_perfil = get_object_or_404(PerfilModel, perfil_link=perfil_link, universidade=universidade)
    imagem = ImagemModel.objects.get(perfil=pag_perfil, is_profile_image=True)
    perfil = PerfilModel.objects.get(usuario=request.user)

    user_membro = MembroModel.objects.filter(usuario=request.user, ativo=True)

    membro = MembroModel.objects.filter(usuario=pag_perfil.usuario)
    interesses = UsuarioInteresseModel.objects.filter(usuario=pag_perfil.usuario, ativo=True)
    amigos = AmigoModel.objects.filter(perfil=pag_perfil, ativo=True)

    amigos_dict = {}

    for amigo in amigos:
        amigos_dict[amigo] = ImagemModel.objects.get(perfil=amigo.amigo, is_profile_image=True)

    postagens = PostagemGrupoModel.objects.filter(criado_por=pag_perfil.usuario, ativo=True,
                                                  grupo__membromodel__in=user_membro).order_by('-data_criacao')
    comentarios = ComentarioGrupoModel.objects.filter(postagem__in=postagens, ativo=True)

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
            qtd = ComentarioGrupoModel.objects.filter(postagem=postagem, ativo=True)
            qtd_comentarios[postagem.pid] = len(qtd)

        if postagem.pid not in comentario_postagem:
            comentario_postagem[postagem.pid] = ComentarioGrupoModel.objects.filter(ativo=True, postagem=postagem)\
                .order_by('-data_criacao')

    try:
        amigo = AmigoModel.objects.get(perfil=perfil, amigo=pag_perfil, ativo=True)

    except AmigoModel.DoesNotExist:
        amigo = None

    try:
        convite_amigo = ConviteAmigoModel.objects.get(perfil=perfil, amigo=pag_perfil, ativo=True)

    except ConviteAmigoModel.DoesNotExist:
        convite_amigo = None

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        if 'removerAmigo' in request.POST:
            amigo_rem1 = AmigoModel.objects.get(perfil=perfil, amigo=pag_perfil)
            amigo_rem2 = AmigoModel.objects.get(perfil=pag_perfil, amigo=perfil)

            amigo_rem1.ativo = False
            amigo_rem1.save()

            amigo_rem2.ativo = False
            amigo_rem2.save()

        if 'adicionarAmigo' in request.POST and not convite_amigo and not amigo:
            convite = ConviteAmigoModel()

            convite.perfil = perfil
            convite.amigo = pag_perfil
            convite.save()

        if 'deleteComment' in request.POST:
            pcid = request.POST['deleteComment'].split('-')

            pid = int(pcid[0])
            cid = int(pcid[1])

            print cid

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

            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                pid = request.POST.get('comentarPostagem')
                postagem = PostagemGrupoModel.objects.get(pid=pid)

                comentario.criado_por = request.user
                comentario.conteudo = request.POST['comentario']
                comentario.postagem = postagem
                comentario.data_criacao = timezone.now()
                comentario.save()

        return HttpResponseRedirect('/perfil/' + universidade.sigla_campus + '/' + pag_perfil.perfil_link)
    else:
        comentario_form = ComentarioGrupoForm()

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['convite_amigo'] = convite_amigo
    args['amigo'] = amigo
    args['qtd_comentarios'] = qtd_comentarios
    args['comentario_form'] = comentario_form
    args['pesquisa_form'] = UsuarioSearchForm(request.GET)
    args['interesses_possui'] = interesses
    args['grupos_participa'] = membro
    args['postagens'] = postagens
    args['fotos_comentarios'] = fotos_comentarios
    args['fotos_postagens'] = fotos_postagens
    args['perfis_postagens'] = perfis_postagens
    args['perfis_comentarios'] = perfis_comentarios
    args['comentario_postagem'] = comentario_postagem
    args['amigos'] = amigos_dict
    args['perfil'] = perfil
    args['foto'] = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)
    args['universidade'] = universidade
    args['grupos_participa'] = membro
    args['interesses_possui'] = interesses
    args['pag_foto'] = imagem
    args['usuario'] = pag_perfil.usuario
    args['pag_perfil'] = pag_perfil
    args['idade'] = calcular_idade(pag_perfil.data_nascimento)
    args['aniversario'] = calcular_aniversario(pag_perfil.data_nascimento)

    args['pesquisa_form'] = UsuarioSearchForm(request.GET)

    return render(request, 'contas/perfil.html', args)


@login_required
def view_perfil_usuario_sobre(request, sigla, perfil_link):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_active=True, is_profile_image=True)

    pag_perfil = PerfilModel.objects.get(perfil_link=perfil_link, universidade__sigla_campus=sigla)
    pag_foto = ImagemModel.objects.get(perfil=pag_perfil, is_active=True, is_profile_image=True)
    interesses = UsuarioInteresseModel.objects.filter(usuario=pag_perfil.usuario, ativo=True)
    grupos = MembroModel.objects.filter(usuario=pag_perfil.usuario, ativo=True)
    amigos = AmigoModel.objects.filter(perfil=pag_perfil, ativo=True)

    amigos_dict = {}

    for amizade in amigos:
        if amizade not in amigos_dict:
            amigos_dict[amizade] = ImagemModel.objects.get(perfil=amizade.amigo, is_profile_image=True)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

    try:
        amigo = AmigoModel.objects.get(perfil=perfil, amigo=pag_perfil, ativo=True)

    except AmigoModel.DoesNotExist:
        amigo = None

    try:
        convite_amigo = ConviteAmigoModel.objects.get(perfil=perfil, amigo=pag_perfil, ativo=True)

    except ConviteAmigoModel.DoesNotExist:
        convite_amigo = None

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['convite_amigo'] = convite_amigo
    args['amigo'] = amigo
    args['interesses'] = interesses
    args['grupos'] = grupos
    args['amigos'] = amigos_dict
    args['pag_foto'] = pag_foto
    args['pag_perfil'] = pag_perfil
    args['usuario'] = pag_perfil.usuario
    args['universidade'] = pag_perfil.universidade
    args['idade'] = calcular_idade(pag_perfil.data_nascimento)
    args['aniversario'] = calcular_aniversario(pag_perfil.data_nascimento)

    args['perfil'] = perfil
    args['foto'] = foto
    args['pesquisa_form'] = UsuarioSearchForm()

    return render(request, 'contas/perfil_sobre.html', args)


@login_required
def view_editar_perfil(request):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True, is_active=True)

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        usuario_form = UsuarioEditForm(data=request.POST)
        perfil_form = PerfilEditForm(data=request.POST)
        foto_form = ImagemUploadForm(files=request.FILES)

        if usuario_form.is_valid() and perfil_form.is_valid() and foto_form.is_valid():
            request.user.first_name = usuario_form.cleaned_data.get('first_name')
            request.user.last_name = usuario_form.cleaned_data.get('last_name')

            dia = perfil_form.cleaned_data.get('dia')
            mes = perfil_form.cleaned_data.get('mes')
            ano = perfil_form.cleaned_data.get('ano')

            data_str = '%s-%s-%s' % (dia, mes, ano)
            perfil.data_nascimento = datetime.strptime(data_str, '%d-%m-%Y')
            perfil.curso = perfil_form.cleaned_data.get('curso')
            perfil.universidade = perfil_form.cleaned_data.get('universidade')

            perfil.save()
            request.user.save()

            if 'imagem' in request.FILES and request.FILES['imagem']:
                foto.is_profile_image = False
                foto.save()

                foto = foto_form.save(commit=False)
                foto.perfil = perfil
                foto.is_profile_image = True

            foto.save()

            return HttpResponseRedirect('/perfil/' + perfil.universidade.sigla_campus + '/' + perfil.perfil_link)
    else:
        usuario_form = UsuarioEditForm()
        perfil_form = PerfilEditForm()
        foto_form = ImagemUploadForm()

        perfil_form.fields['universidade'].initial = perfil.universidade
        perfil_form.fields['curso'].initial = perfil.curso
        perfil_form.fields['dia'].initial = perfil.data_nascimento.day
        perfil_form.fields['mes'].initial = perfil.data_nascimento.month
        perfil_form.fields['ano'].initial = perfil.data_nascimento.year
        usuario_form.fields['first_name'].initial = request.user.first_name
        usuario_form.fields['last_name'].initial = request.user.last_name

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['foto_form'] = foto_form
    args['usuario_form'] = usuario_form
    args['perfil_form'] = perfil_form
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)
    args['foto'] = foto
    args['idade'] = calcular_idade(perfil.data_nascimento)
    args['aniversario'] = calcular_aniversario(perfil.data_nascimento)

    return render(request, 'contas/perfil_editar.html', args)

@login_required
def view_desativar_perfil(request):
    # TODO view para desativar perfil com: desativação de todos os tokens +
    # TODO confirmação da desativação reinformando e-mail e senha
    pass