# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v004a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002, RF020, RF022, RF023, RF027
Caso(s) de Uso: DV001, DV002, DVA012

Descrição:
    Definição das views relacionadas à aplicação de contas (cadastro/login).
"""

from contas.forms import UsuarioCadastroForm, PerfilCadastroForm, UsuarioLoginForm, EnviarTokenForm, SenhaResetForm
from universidades.models import UniversidadeModel
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout
from datetime import datetime, timedelta
from django.utils import timezone
from contas.models import PerfilModel, UsuarioModel, TokenModel
from contas import methods
from django.contrib.auth.decorators import login_required
from contas import constants
from mainAcad.forms import UsuarioSearchForm


def view_cadastrar_usuario(request):
    args = {}

    # Se o usuário já estiver logado, ele será redirecionado para a página inicial

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        usuario_form = UsuarioCadastroForm(data=request.POST)
        perfil_form = PerfilCadastroForm(data=request.POST)

        if usuario_form.is_valid() and perfil_form.is_valid():

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

            token = methods.gerar_token(constants.TOKEN_TYPE[0], usuario, token, email,
                                        timezone.now() + timedelta(days=7))

            # Salvando a foto (caso esta tenha sido definida) e renomeando-a.

            if 'foto' in request.FILES:
                foto = request.FILES['foto']
                foto.name = methods.gerar_nome_imagem(usuario.uid)
                perfil.foto = foto

            # Formatação da data de nascimento do usuário

            dia = perfil_form.cleaned_data['dia']
            mes = perfil_form.cleaned_data['mes']
            ano = perfil_form.cleaned_data['ano']

            data_str = '%s-%s-%s' % (dia, mes, ano)
            perfil.data_nascimento = datetime.strptime(data_str, '%d-%m-%Y')

            # Finalização das configurações do perfil de usuário -> perfil salvo

            perfil.save()

            # Enviando e-mail de validação da conta para o usuário

            methods.enviar_email_ativacao(email, nome, sobrenome, token.token)

            args['usuario'] = usuario

            return render(request, 'contas/cadastro_sucesso.html', args)
    else:
        usuario_form = UsuarioCadastroForm()
        perfil_form = PerfilCadastroForm()
        args['usuario'] = None

    args['usuario_form'] = usuario_form
    args['perfil_form'] = perfil_form

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

            return redirect(methods.redirect_to_next(request.get_full_path()))
        else:
            return view_login_usuario(request)
    else:
        login_form = UsuarioLoginForm(request)

    args['login_form'] = login_form

    return render(request, 'contas/index.html', args)


def view_pagina_inicial_logada(request):
    args = {}

    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')

    perfil = PerfilModel.objects.get(usuario=request.user)
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(request.GET)

    return render(request, 'contas/home.html', args)


def view_login_usuario(request):
    args = {}

    # Checa se o usuário já está logado.

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        login_form = UsuarioLoginForm(data=request.POST)

        # Caso o login ocorra de forma correta (campos corretos).

        if login_form.is_valid():
            login(request, login_form.get_usuario())

            # Se o usuário for um superuser, este será redirecionado para a página de admin.

            if request.user.is_superuser:
                return HttpResponseRedirect('/admin')

            # Se for um usuário normal, ele será mandado para a view da página principal.

            return redirect(methods.redirect_to_next(request.get_full_path()))

    else:
        login_form = UsuarioLoginForm(request)

    args['login_form'] = login_form

    return render(request, 'contas/login.html', args)


def view_logout_usuario(request):
    logout(request)

    return HttpResponseRedirect('/')


def view_confirmar_usuario(request, chave):
    args = {}

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
            novo_token = methods.gerar_token(constants.TOKEN_TYPE[0], usuario, novo_token, email,
                                             timezone.now() + timedelta(days=7))

            # Envia um novo e-mail de ativação para o usuário

            methods.enviar_email_ativacao(email, usuario.first_name, usuario.last_name, novo_token.token)

            args['email'] = email

            # O token anterior passa a ser inválido, para que não possa ser acessado novamente.

            token.valid = False
            token.save()

            return render(request, 'contas/cadastro_email_ativacao.html', args)
    else:
        ativacao_form = EnviarTokenForm()

        # Define o valor do campo 'email' para o e-mail do usuário que acessou a página.

        ativacao_form.fields['email'].widget.attrs['value'] = token.usuario.email

    args['expired'] = not token.active
    args['ativacao_form'] = ativacao_form

    return render(request, 'contas/cadastro_confirmar.html', args)


def view_senha_reset(request):
    args = {}

    if request.method == 'POST':
        senha_form = EnviarTokenForm(data=request.POST)

        if senha_form.is_valid():

            # Resgata as informações do usuário que requisitou a redefinição de senha.

            email = senha_form.cleaned_data['email']
            usuario = UsuarioModel.object.get(email=email)

            # Gera um token de redefinição de senha.

            token = TokenModel()
            token = methods.gerar_token(constants.TOKEN_TYPE[1], usuario, token, email)
            methods.enviar_email_senha_reset(token, usuario, email)

            return render(request, 'contas/senha_reset_completo.html', args)
    else:
        senha_form = EnviarTokenForm()

    args['senha_form'] = senha_form

    return render(request, 'contas/senha_reset.html', args)


def view_senha_reset_confirmado(request, uid, chave):
    args = {}

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

            return render(request, 'contas/senha_reset_finalizado.html', args)

    else:
        senha_form = SenhaResetForm()

    args['expired'] = not token.active
    args['senha_form'] = senha_form

    return render(request, 'contas/senha_reset_confirmado.html', args)


def view_reativar_usuario(request):
    args = {}

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
            novo_token = methods.gerar_token(constants.TOKEN_TYPE[0], usuario, novo_token, email,
                                             timezone.now() + timedelta(days=7))

            # Envia um novo e-mail de ativação para o usuário

            methods.enviar_email_ativacao(email, usuario.first_name, usuario.last_name, novo_token.token)

            args['finalizado'] = True

    else:
        reativar_form = EnviarTokenForm()
        args['finalizado'] = False

    args['reativar_form'] = reativar_form

    return render(request, 'contas/cadastro_reativar.html', args)


@login_required
def view_perfil_usuario(request, sigla, perfil_link):
    args = {}

    # Procura por um usuário e perfil existente que pertença ao link dado.

    sigla = sigla.upper()

    universidade = get_object_or_404(UniversidadeModel, sigla=sigla)
    perfil = get_object_or_404(PerfilModel, perfil_link=perfil_link, universidade=universidade)

    args['usuario'] = perfil.usuario
    args['perfil'] = perfil
    args['idade'] = methods.calcular_idade(perfil.data_nascimento)
    args['aniversario'] = methods.calcular_aniversario(perfil.data_nascimento)

    return render(request, 'contas/perfil.html', args)


def view_desativar_perfil(request):
    # TODO view para desativar perfil com: desativação de todos os tokens +
    # TODO confirmação da desativação reinformando e-mail e senha
    pass