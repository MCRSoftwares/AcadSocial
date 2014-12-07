# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002, RF022
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das views relacionadas à aplicação de contas (cadastro/login).
"""

from contas.forms import UsuarioCadastroForm, PerfilCadastroForm, UsuarioLoginForm
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout
from datetime import datetime
from contas.models import PerfilModel, UsuarioModel
import contas.methods as methods
from django.contrib.auth.decorators import login_required
import hashlib
import random


def view_cadastrar_usuario(request):
    args = {}

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        usuario_form = UsuarioCadastroForm(data=request.POST)
        perfil_form = PerfilCadastroForm(data=request.POST)

        if usuario_form.is_valid() and perfil_form.is_valid():

            # Passando as informações do formuário para seus respectivos modelos.
            usuario = usuario_form.save()
            usuario.email = usuario_form.cleaned_data['email']

            usuario.set_password(usuario.password)
            usuario.save()

            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario

            # Geração da chave de ativação do usuário.

            email = usuario.email
            nome = usuario_form.cleaned_data['first_name']
            sobrenome = usuario_form.cleaned_data['last_name']

            hash_salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            chave = hashlib.sha1(hash_salt+email).hexdigest()
            perfil.chave_ativacao = chave

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

            email_assunto = 'AcadSocial - Confirme seu e-mail'

            email_conteudo = 'Bem-vindo, %s %s.\nAgradecemos o seu cadastro no AcadSocial!\n' \
                             'Clique no link abaixo para confirmar o seu e-mail e utilizar nossa rede!' \
                             '\nhttp://127.0.0.1:8000/perfil/ativar/%s' % (nome, sobrenome, chave)

            send_mail(email_assunto, email_conteudo, None, [email], fail_silently=False)

            args['usuario'] = usuario

            # TODO criar template para confirmação de cadastro
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

    # Checa se o usuário já está logado

    if request.user.is_authenticated():
        return view_pagina_inicial_logada(request)

    if request.method == 'POST':
        login_form = UsuarioLoginForm(data=request.POST)

        # Caso o login ocorra de forma correta (campos corretos)

        if login_form.is_valid():
            login(request, login_form.get_usuario())

            # Se o usuário for um superuser, este será redirecionado para a página de admin

            if request.user.is_superuser:
                return HttpResponseRedirect('/admin')

            # Se for um usuário normal, ele será mandado para a view da página principal

            return redirect(methods.redirect_to_next(request.get_full_path()))
        else:
            return view_login_usuario(request)
    else:
        login_form = UsuarioLoginForm(request)

    args['login_form'] = login_form

    return render(request, 'contas/index.html', args)


def view_pagina_inicial_logada(request):
    args = {}

    return render(request, 'contas/home.html', args)


def view_login_usuario(request):
    args = {}

    # Checa se o usuário já está logado

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        login_form = UsuarioLoginForm(data=request.POST)

        # Caso o login ocorra de forma correta (campos corretos)

        if login_form.is_valid():
            login(request, login_form.get_usuario())

            # Se o usuário for um superuser, este será redirecionado para a página de admin

            if request.user.is_superuser:
                return HttpResponseRedirect('/admin')

            # Se for um usuário normal, ele será mandado para a view da página principal

            return redirect(methods.redirect_to_next(request.get_full_path()))

    else:
        login_form = UsuarioLoginForm(request)

    args['login_form'] = login_form

    return render(request, 'contas/login.html', args)


def view_logout_usuario(request):
    logout(request)

    return HttpResponseRedirect('/')


def view_confirmar_usuario(request, chave):

    if request.user.is_authenticated():
        # Se o usuário já estiver logado, ele será redirecionado para a página inicial.

        return HttpResponseRedirect('/')

    # Confere se existe algum perfil que possui a chave dada. Caso não exista, o sistema retorna 404.
    perfil = get_object_or_404(PerfilModel, chave_ativacao=chave)
    perfil.chave_ativacao = ''
    perfil.save()

    usuario = perfil.usuario
    usuario.is_active = True
    usuario.save()

    # TODO criar template para a ativação da conta
    return HttpResponse('Sua conta foi ativada!')


@login_required
def view_perfil_usuario(request, uid, perfil_link):
    args = {}

    usuario = get_object_or_404(UsuarioModel, uid=uid, perfil_link=perfil_link)

    if not usuario.is_active:
        # TODO criar template de usuario inativo
        return HttpResponseRedirect('/')

    perfil = get_object_or_404(PerfilModel, usuario=usuario)

    args['usuario'] = usuario
    args['perfil'] = perfil
    args['idade'] = methods.calcular_idade(perfil.data_nascimento)
    args['aniversario'] = methods.calcular_aniversario(perfil.data_nascimento)

    return render(request, 'contas/perfil.html', args)