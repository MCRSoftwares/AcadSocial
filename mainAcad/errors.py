# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das mensagens de erro relacionados à aplicação principal.
"""

from mainAcad.constants import MAX_IMAGE_SIZE

# Erros relacionados ao forms.py

erro_imagem = {
    'limite_tamanho': 'A imagem deve ter no máximo %s.%sMB!' % (str(MAX_IMAGE_SIZE)[0], str(MAX_IMAGE_SIZE)[1]),
}