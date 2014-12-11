# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das constantes relacionadas à aplicação de contas (cadastro/login).
"""

VALID_EMAILS = (
    '@ufpe.br',
)

TOKEN_TYPE = (
    'email_ativacao',
    'senha_reset',
)

MAX_IMAGE_SIZE = 4*1024*1024