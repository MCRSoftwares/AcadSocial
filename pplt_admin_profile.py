# -*- encoding: utf-8 -*-

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AcadSocial.settings')

django.setup()

from contas.models import PerfilModel, UsuarioModel
from mainAcad.models import ImagemModel
from universidades.models import UniversidadeModel, CursoModel
from datetime import datetime


def populate():
    usuario = add_usuario('AcadSocial', 'Team', 'AcadSocial@acadsocial.admin', 'AAEDV2015', True, True, True)
    perfil = add_perfil(usuario, 'UFPERecife', u'Sistemas de Informação', '26-01-2015')
    add_imagem(True, perfil)


def add_perfil(usuario, universidade, univ_curso, data_nasc):
    univ = UniversidadeModel.objects.get(sigla_campus=universidade)
    curso = CursoModel.objects.get(universidade=univ, nome=univ_curso)
    perfil = PerfilModel.objects.get_or_create(universidade=univ, curso=curso, usuario=usuario,
                                               data_nascimento=datetime.strptime(data_nasc, '%d-%m-%Y'))[0]
    return perfil


def add_usuario(nome, sobrenome, email, senha, is_staff, is_superuser, is_active):
    usuario = UsuarioModel.object.get_or_create(first_name=nome, last_name=sobrenome, email=email,
                                                is_staff=is_staff, is_superuser=is_superuser, is_active=is_active)[0]
    usuario.set_password(senha)
    usuario.save()

    return usuario


def add_imagem(is_profile_image, perfil):
    imagem = ImagemModel.objects.get_or_create(is_profile_image=is_profile_image, perfil=perfil,
                                               imagem='imagens/perfil/acadsocial.jpg')[0]
    return imagem

if __name__ == '__main__':
    print 'Populating...'
    populate()
    print 'Done!'