# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002, RF020, RF022, RF023, RF027
Caso(s) de Uso: DV001, DV002, DVA012

Descrição:
    Definição dos métodos auxiliares relacionados à aplicação de contas (cadastro/login).
"""

from datetime import datetime
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from AcadSocial.settings import SYSTEM_HOST
import hashlib
import random
import re


def gerar_chave(param):

    """
    Gera um hash baseado num valor random e soma com uma
    chave baseada num parâmetro passado para esta função.
    """

    hash_salt = hashlib.sha256(str(random.random())).hexdigest()[:5]
    chave = hashlib.sha256(hash_salt+param).hexdigest()

    return chave


def calcular_idade(data):

    """
    Calcula a idade do usuário através de sua data de nascimento e da data atual.
    """

    hoje = datetime.today()

    return hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))


def calcular_aniversario(data):

    """
    Recupera somente o mês e o dia do aniversário do usuário
    """

    dia = str(data.day)
    mes = str(data.month)

    if data.day < 10:
        dia = '0' + str(data.day)

    if data.month < 10:
        mes = '0' + str(data.month)

    return str(dia) + '/' + str(mes)


def selecionar_inicio_email(email):

    """
    Separa o e-mail em duas partes pelo @,
    utilizado para criação do link do perfil do usuário
    """

    divisao = str(email).index('@')
    inicio = str(email)[0:divisao]

    return inicio


def selecionar_final_email(email):

    """
    Separa o e-mail em duas partes pelo @,
    utilizado para criação do link do perfil do usuário
    """

    divisao_inicio = str(email).index('@')
    divisao_fim = str(email).rindex('.')
    inicio = str(email)[divisao_inicio:divisao_fim]

    return inicio


def redirecionar_para(path):

    """
    Checa se há um redirecionamento requisitado após o login do usuário.
    """

    if '?next=/' in path:
        path = path[path.index('?next=/') + 6:]
        return path

    return '/'


def enviar_email_ativacao(email, nome, sobrenome, chave):

    """
    Envia um e-mail de ativação ao usuário que solicitou o cadastro.
    """

    # TODO criar um título e conteúdo melhor para o e-mail de ativação

    email_assunto = '[AcadSocial] Confirme seu E-mail!'

    email_conteudo = 'Bem-vindo, %s %s.\nAgradecemos o seu cadastro no AcadSocial!\n' \
                     'Clique no link abaixo para confirmar o seu e-mail e utilizar nossa rede!' \
                     '\nhttp://%s/conta/ativar/%s' % (nome, sobrenome, SYSTEM_HOST, chave)

    email_msg = EmailMessage(email_assunto, email_conteudo, to=[email])
    email_msg.send()


def enviar_email_senha_reset(token, usuario, email):

    """
    Envia um e-mail de redefinição de senha para o usuário que a solicitou.
    """

    # TODO criar um título e conteúdo melhor para o e-mail de redefinição de senha

    email_assunto = '[AcadSocial] Redefinição de senha'

    email_conteudo = 'Fora solicitado um pedido de redefinição da senha de sua conta no AcadSocial.' \
                     ' Caso você não tenha pedido a redefinição de senha, por favor ignore este e-mail.\n\n' \
                     'Caso contrário, acesse o link abaixo para redefinir sua senha: \n ' \
                     'http://%s/conta/senha/%s/%s' % (SYSTEM_HOST, usuario.uid, token.token)

    email_msg = EmailMessage(email_assunto, email_conteudo, to=[email])
    email_msg.send()


def gerar_token(tipo, usuario, token, token_param, data=None):

    """
    Preenche os atribudos de models.TokenModel(), incluindo a chave em si.
    """

    token.usuario = usuario
    token.token = gerar_chave(token_param)
    token.tipo = tipo

    if data:
        token.data_expiracao = data

    token.save()

    return token


def validar_senhas(senha, senha_conf):

    """
    Confere se as senhas estão válidas e retorna o tipo de erro caso não esteja.
    """

    if senha and not re.match('^\S*(?=\S*[a-zA-Z])(?=\S*[0-9])\S{6,20}$', senha):

        # A senha deve conter pelo menos 6 caracteres, tendo pelo menos 1 letra e 1 número.

        return 'invalida'

    if senha != senha_conf:
        return 'diferentes'

    return 'correta'


def validar_palavra(palavra):

    """
    Confere se a palavra contém somente caracteres válidos (não numéricos).
    """

    if palavra and re.match('^\S*(?=\S*[0-9])\S$', palavra):
        return False

    return True


def login_form_body(request, view_login_usuario, login_form, login):

    if login_form.is_valid():
        login(request, login_form.get_usuario())

        # Se o usuário for um superuser, este será redirecionado para a página de admin.

        if request.user.is_superuser:
            return HttpResponseRedirect('/admin')

        # Se for um usuário normal, ele será mandado para a view da página principal.

        return redirect(redirecionar_para(request.get_full_path()))
    else:
        return view_login_usuario(request)