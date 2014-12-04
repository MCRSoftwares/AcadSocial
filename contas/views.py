# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v01a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das views relacionadas à aplicação de contas (cadastro/login).
"""

from contas.forms import UsuarioCadastroForm, PerfilCadastroForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import contas.methods as methods
import hashlib
import random


def view_cadastrar_usuario(request):
    args = {}
    cadastrado = False

    if request.method == 'POST':
        usuario_form = UsuarioCadastroForm(data=request.POST)
        perfil_form = PerfilCadastroForm(data=request.POST)

        if usuario_form.is_valid() and perfil_form.is_valid():

            # Passando as informações do formuário para seus respectivos modelos.

            usuario = usuario_form.save()
            perfil = perfil_form.save(commit=False)

            usuario.set_password(usuario.password)
            usuario.save()

            perfil.usuario = usuario

            # Geração da chave de ativação do usuário.

            email = usuario_form.cleaned_data['email']

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

            # TODO criar um assunto para o e-mail
            email_assunto = ''
            # TODO criar um conteúdo para o e-mail
            email_conteudo = ''

            send_mail(email_assunto, email_conteudo, None, [email], fail_silently=False)

            cadastrado = True
    else:
        usuario_form = UsuarioCadastroForm()
        perfil_form = PerfilCadastroForm()

    args['usuario_form'] = usuario_form
    args['perfil_form'] = perfil_form
    args['cadastrado'] = cadastrado

    return render(request, 'contas/cadastro.html', args)


def view_pagina_inicial(request):
    args = {}

    # TODO criar view para a página inicial
    return render(request, 'contas/index.html', args)


def view_login_usuario(request):
    args = {}

    # TODO criar view para a página de login
    return render(request, 'contas/login.html', args)