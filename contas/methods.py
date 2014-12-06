# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição dos métodos auxiliares relacionados à aplicação de contas (cadastro/login).
"""

from datetime import datetime
import hashlib


def gerar_nome_imagem(random_id):
    data = datetime.today()
    data_f = data.strftime('%Y%m%d%H%M%S')

    nome_foto = str(data_f) + '-' + str(random_id) + str(hashlib.sha1(str(data)).hexdigest()[0:15])

    return nome_foto + '.jpg'


def calcular_idade(data):
    hoje = datetime.today()

    return hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))


def calcular_aniversario(data):
    dia = str(data.day)
    mes = str(data.month)

    if data.day < 10:
        dia = '0' + str(data.day)

    if data.month < 10:
        mes = '0' + str(data.month)

    return str(dia) + '/' + str(mes)


def selecionar_inicio_email(email):
    divisao = str(email).index('@')
    inicio = str(email)[0:divisao]

    return inicio