# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição dos métodos auxiliares relacionados à aplicação de grupos/eventos.
"""
from grupos.models import ConviteGrupoModel, ConviteEventoModel, MembroModel, ParticipaEventoModel
from mainAcad.models import ImagemModel, ConviteAmigoModel, AmigoModel


def load_convites_grupos(request):
    convites_grupos = ConviteGrupoModel.objects.filter(convidado=request.user, ativo=True)
    convites_grupos_dict = {}

    for convite in convites_grupos:
        if convite not in convites_grupos_dict:
            convites_grupos_dict[convite] = ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                                                    perfil__usuario=convite.usuario)

    return convites_grupos_dict


def load_convites_eventos(request):
    convites_eventos = ConviteEventoModel.objects.filter(convidado=request.user, ativo=True)
    convites_eventos_dict = {}

    for convite in convites_eventos:
        if convite not in convites_eventos_dict:
            convites_eventos_dict[convite] = ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                                                     perfil__usuario=convite.usuario)

    return convites_eventos_dict


def load_convites_amigos(perfil):
    convites_amigos = ConviteAmigoModel.objects.filter(amigo=perfil, ativo=True)
    convites_amigos_dict = {}

    for convite in convites_amigos:
        if convite not in convites_amigos_dict:
            convites_amigos_dict[convite] = ImagemModel.objects.get(is_profile_image=True, is_active=True,
                                                                    perfil=convite.perfil)

    return convites_amigos_dict


def convites_amigos_post(request, html_id):

    if html_id in request.POST:
        action = request.POST.get(html_id)
        cid = action.split('-')[1]

        if action.startswith('aceitar'):
            convite_amigo = ConviteAmigoModel.objects.get(cid=cid, ativo=True)
            convite_amigo.ativo = False
            convite_amigo.save()

            check_amigo_model(convite_amigo.amigo, convite_amigo.perfil)
            check_amigo_model(convite_amigo.perfil, convite_amigo.amigo)

        elif action.startswith('recusar'):
            convite_amigo = ConviteAmigoModel.objects.get(cid=cid, ativo=True)
            convite_amigo.ativo = False
            convite_amigo.save()


def convites_grupos_post(request, html_id):

    if html_id in request.POST:

        action = request.POST.get(html_id)
        cid = action.split('-')[1]

        if action.startswith('aceitar'):
            convite_grupo = ConviteGrupoModel.objects.get(cid=cid, ativo=True)
            convite_grupo.ativo = False
            convite_grupo.aceito = True
            convite_grupo.save()

            try:
                membro = MembroModel.objects.get(grupo=convite_grupo.grupo, usuario=convite_grupo.convidado)
                membro.ativo = True
                membro.save()

            except MembroModel.DoesNotExist:
                membro = MembroModel()
                membro.grupo = convite_grupo.grupo
                membro.usuario = convite_grupo.convidado
                membro.save()

        elif action.startswith('recusar'):
            convite_grupo = ConviteGrupoModel.objects.get(cid=cid)
            convite_grupo.ativo = False
            convite_grupo.save()


def convites_eventos_post(request, html_id):

    if html_id in request.POST:

        action = request.POST.get(html_id)
        cid = action.split('-')[1]

        if action.startswith('aceitar'):
            convite_evento = ConviteEventoModel.objects.get(cid=cid, ativo=True)
            convite_evento.ativo = False
            convite_evento.aceito = True
            convite_evento.save()

            try:
                participa = ParticipaEventoModel.objects.get(evento=convite_evento.evento,
                                                             usuario=convite_evento.convidado)
                participa.ativo = True
                participa.save()

            except ParticipaEventoModel.DoesNotExist:
                participa = ParticipaEventoModel()
                participa.usuario = convite_evento.convidado
                participa.evento = convite_evento.evento
                participa.save()

        elif action.startswith('recusar'):
            convite_evento = ConviteEventoModel.objects.get(cid=cid, ativo=True)
            convite_evento.ativo = False
            convite_evento.save()


def check_amigo_model(c_amigo, c_perfil):

    try:
        amigo = AmigoModel.objects.get(amigo=c_perfil, perfil=c_amigo)
        amigo.ativo = True
        amigo.save()

    except AmigoModel.DoesNotExist:
        amigo = AmigoModel()
        amigo.perfil = c_amigo
        amigo.amigo = c_perfil
        amigo.save()