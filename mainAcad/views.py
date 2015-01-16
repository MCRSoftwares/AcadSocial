# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v001a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das views relacionadas à aplicação principal.
"""

from django.shortcuts import render
from mainAcad.forms import UsuarioSearchForm
from contas.models import PerfilModel
from grupos.models import GrupoModel, InteresseModel, EventoModel
from grupos.models import PostagemGrupoModel, PostagemEventoModel
from django.db.models import Q
from mainAcad.models import ImagemModel


def view_usuario_search(request):
    args = {}

    # TODO criar uma forma de pesquisa completa (esta serve somente para resgatar perfil de usuários)
    # TODO alterar forma em que os dados são salvos: tudo em lowerCase, para ajudar na pesquisa.

    if request.GET.get('q'):
        pesquisa_form = UsuarioSearchForm(data=request.GET)

        if pesquisa_form.is_valid():
            data = pesquisa_form.cleaned_data['q']
            lista = data.split(' ')
            
            data_list = filter(None, lista)

            resultado = False
            perfis_dict = {}
            grupos = None
            interesses = None
            eventos = None
            postagens_grupos = None
            postagens_eventos = None

            for item in data_list:

                if request.GET.get('f'):
                    filtro = request.GET.get('f')
                    args['filtro'] = filtro

                    if filtro == '1':
                        perfil_query = Q(usuario__first_name__contains=item) | Q(usuario__last_name__contains=item)
                        perfis = PerfilModel.objects.filter(perfil_query).order_by('usuario_id')

                        if perfis:
                            resultado = True
                            for perfil in perfis:
                                perfis_dict[perfil] = ImagemModel.objects.get(perfil=perfil)

                    elif filtro == '2':
                        grupo_query = Q(nome__contains=item) | Q(descricao__contains=item)
                        grupos = GrupoModel.objects.filter(grupo_query)

                        if grupos:
                            resultado = True

                    elif filtro == '3':
                        interesse_query = Q(interesse__contains=item)
                        interesses = InteresseModel.objects.filter(interesse_query)

                        if interesses:
                            resultado = True

                    elif filtro == '4':
                        evento_query = Q(titulo__contains=item) | Q(descricao__contains=item)
                        eventos = EventoModel.objects.filter(evento_query)

                        if eventos:
                            resultado = True

                    elif filtro == '5':
                        postagem_query = Q(titulo__contains=item) | Q(conteudo__contains=item)
                        postagens_grupos = PostagemGrupoModel.objects.filter(postagem_query)
                        postagens_eventos = PostagemEventoModel.objects.filter(postagem_query)

                        if postagens_eventos and postagens_grupos:
                            resultado = True

                elif not request.GET.get('f') or request.GET.get('f') == '0':
                    perfil_query = Q(usuario__first_name__contains=item) | Q(usuario__last_name__contains=item)
                    grupo_query = Q(nome__contains=item) | Q(descricao__contains=item)
                    interesse_query = Q(interesse__contains=item)
                    evento_query = Q(titulo__contains=item) | Q(descricao__contains=item)
                    postagem_query = Q(titulo__contains=item) | Q(conteudo__contains=item)

                    perfis = PerfilModel.objects.filter(perfil_query).order_by('usuario_id')

                    if perfis:
                        for perfil in perfis:
                            perfis_dict[perfil] = ImagemModel.objects.get(perfil=perfil)

                    grupos = GrupoModel.objects.filter(grupo_query)
                    interesses = InteresseModel.objects.filter(interesse_query)
                    eventos = EventoModel.objects.filter(evento_query)
                    postagens_grupos = PostagemGrupoModel.objects.filter(postagem_query)
                    postagens_eventos = PostagemEventoModel.objects.filter(postagem_query)

                    if grupos or interesses or eventos or postagens_eventos or postagens_grupos or perfis:
                        resultado = True

            args['resultado'] = resultado
            args['perfis'] = perfis_dict
            args['grupos'] = grupos
            args['interesses'] = interesses
            args['eventos'] = eventos
            args['postagens_grupos'] = postagens_grupos
            args['postagens_eventos'] = postagens_eventos
            args['pesquisa'] = data

    else:
        pesquisa_form = UsuarioSearchForm()

    args['pesquisa_form'] = pesquisa_form
    args['perfil'] = PerfilModel.objects.get(usuario=request.user)
    args['foto'] = ImagemModel.objects.get(perfil__usuario=request.user, is_profile_image=True)

    return render(request, 'mainAcad/search.html', args)


def view_lista_amigos(request):
    args = {}

    perfil = PerfilModel.objects.get(usuario=request.user)
    foto = ImagemModel.objects.get(perfil=perfil, is_profile_image=True)

    args['foto'] = foto
    args['perfil'] = perfil
    args['pesquisa_form'] = UsuarioSearchForm(data=request.GET)

    return render(request, 'mainAcad/lista_amigos.html', args)