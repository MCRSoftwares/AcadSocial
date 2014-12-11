# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002, RF020, RF022, RF023, RF027
Caso(s) de Uso: DV001, DV002, DVA012

Descrição:
    Definição dos métodos auxiliares relacionados à aplicação de contas (cadastro/login).
"""

from datetime import datetime
from django.core.mail import send_mail
from PIL import Image
import hashlib
import random
import re
from AcadSocial.settings import MEDIA_ROOT


def gerar_chave(param):

    """
    Gera um hash baseado num valor random e soma com uma
    chave baseada num parâmetro passado para esta função.
    """

    hash_salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    chave = hashlib.sha1(hash_salt+param).hexdigest()

    return chave


def gerar_nome_imagem(random_id):

    """
    Gera um nome para a foto utilizando a hora/data em que fora postada,
    junto do id do usuário que a postou e um hash aleatório baseado na data da postagem.
    """

    data = datetime.today()
    data_f = data.strftime('%Y%m%d%H%M%S')

    nome_foto = str(data_f) + str(random_id)

    return nome_foto + '.jpg'


def converter_para_jpg(imagem_path, uid):

    """
    Converte a imagem hospedada pelo usuário para JPEG.
    """

    imagem = Image.open(imagem_path)

    nova_imagem = Image.new("RGB", imagem.size, (255, 255, 255))
    nova_imagem.paste(imagem)

    imagem_name = gerar_nome_imagem(uid)
    nova_imagem_path = str(MEDIA_ROOT + '\\imagens\\perfil\\' + imagem_name)

    nova_imagem.save(nova_imagem_path, 'JPEG', quality=80)

    return imagem_name


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

    email_assunto = 'AcadSocial - Confirme seu e-mail'

    email_conteudo = 'Bem-vindo, %s %s.\nAgradecemos o seu cadastro no AcadSocial!\n' \
                     'Clique no link abaixo para confirmar o seu e-mail e utilizar nossa rede!' \
                     '\nhttp://127.0.0.1:8000/conta/ativar/%s' % (nome, sobrenome, chave)

    send_mail(email_assunto, email_conteudo, None, [email], fail_silently=False)


def enviar_email_senha_reset(token, usuario, email):

    """
    Envia um e-mail de redefinição de senha para o usuário que a solicitou.
    """

    email_assunto = 'Redefinição da senha'
    email_conteudo = 'http://127.0.0.1:8000/conta/senha/%s/%s' % (usuario.uid, token.token)

    send_mail(email_assunto, email_conteudo, None, [email], fail_silently=False)


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