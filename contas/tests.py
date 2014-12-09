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
from contas.forms import UsuarioCadastroForm, PerfilCadastroForm
from django.utils import timezone
from django_webtest import WebTest
from django_dynamic_fixture import G
from django.core.urlresolvers import reverse
import contas


class UsuarioCadastroTestCase(TestCase):

    def test_usuario_cadastro_model(self):
        usuario1 = G(UsuarioModel)
        usuario2 = G(UsuarioModel)

        usuarios = UsuarioModel.object.all()
        self.assertEquals(usuarios.count(), 2)

        usuario1 = usuario1.__dict__.values()
        usuario0 = usuarios[0].__dict__.values()

        # Remove o 'ModelState', que é diferente para cada objeto (mesmo que seja igual a outro).
        del usuario1[4]
        del usuario0[4]

        for i in range(0, len(usuario1)):
            self.assertEquals(usuario0[i], usuario1[i])

        usuario2 = usuario2.__dict__.values()
        usuario0 = usuarios[1].__dict__.values()

        # Remove o 'ModelState', que é diferente para cada objeto (mesmo que seja igual a outro).
        del usuario2[4]
        del usuario0[4]

        for i in range(0, len(usuario2)):
            self.assertEquals(usuario0[i], usuario2[i])