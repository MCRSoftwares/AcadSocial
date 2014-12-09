# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição dos casos de testes relacionados à aplicação de contas (cadastro/login).
    Inclui os modelos: PerfilModel, UsuarioModel e UsuarioManager.
"""

from django.test import TestCase
from contas.models import PerfilModel, UsuarioModel, TokenModel
