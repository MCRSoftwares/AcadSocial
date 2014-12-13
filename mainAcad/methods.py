# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002, RF020, RF022, RF023, RF027
Caso(s) de Uso: DV001, DV002, DVA012

Descrição:
    Definição dos métodos auxiliares relacionados à aplicação principal.
"""

from datetime import datetime
from AcadSocial.settings import MEDIA_ROOT
from PIL import Image
import hashlib
import random


def gerar_chave_imagem(param):

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

    nome_foto = str(data_f) + gerar_chave_imagem(str(random_id))[:5]

    return nome_foto + '.jpg'


def converter_para_jpg(imagem_path, media_path):

    """
    Converte a imagem hospedada pelo usuário para JPEG.
    """

    imagem = Image.open(imagem_path)

    nova_imagem = Image.new("RGB", imagem.size, (255, 255, 255))
    nova_imagem.paste(imagem)

    imagem_name = gerar_nome_imagem(imagem_path)
    nova_imagem_path = str(MEDIA_ROOT + media_path + imagem_name)

    nova_imagem.save(nova_imagem_path, 'JPEG', quality=95)

    return media_path[1:] + imagem_name