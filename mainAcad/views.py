# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v004a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição das views relacionadas à aplicação principal.
"""

from django.shortcuts import render
from mainAcad.forms import UsuarioSearchForm, ContatoForm
from contas.models import PerfilModel
from grupos.models import GrupoModel, InteresseModel, EventoModel
from grupos.models import PostagemGrupoModel, PostagemEventoModel
from django.db.models import Q
from django.http import HttpResponseRedirect
from mainAcad.models import ImagemModel
from django.contrib.auth.decorators import login_required
from grupos.methods import load_convites_grupos, load_convites_amigos, load_convites_eventos
from grupos.methods import convites_amigos_post, convites_grupos_post, convites_eventos_post


@login_required
def view_usuario_search(request):
    args = {}

    # TODO criar uma forma de pesquisa completa (esta serve somente para resgatar perfil de usuários)
    # TODO alterar forma em que os dados são salvos: tudo em lowerCase, para ajudar na pesquisa.

    if request.GET.get('q'):
        pesquisa_form = UsuarioSearchForm(data=request.GET)

        if pesquisa_form.is_valid():
            data = pesquisa_form.cleaned_data.get('q')
            args['data_list'] = data

            aspas = data.count('\"')

            if aspas > 0:
                if aspas % 2 == 0:
                    data_list = [q_data for q_data in data.split('\"') if q_data.strip()]
                else:
                    data_list = [data.replace('\"', '')]

            else:
                data_list = [data]

            resultado = False
            perfis_dict = {}
            grupos = None
            interesses = None
            eventos = None
            postagens_grupos = None
            postagens_eventos = None

            for item in data_list:

                if request.GET.get('f') and not request.GET.get('f') == '0':
                    filtro = request.GET.get('f')
                    args['filtro'] = filtro

                    if filtro == '1':
                        perfil_query = Q(usuario__full_name__icontains=item)
                        perfis = PerfilModel.objects.filter(perfil_query)

                        if perfis:
                            resultado = True
                            for perfil in perfis:
                                perfis_dict[perfil] = ImagemModel.objects.get(perfil=perfil)

                    elif filtro == '2':
                        grupo_query = Q(nome__icontains=item)
                        grupos = GrupoModel.objects.filter(grupo_query, ativo=True)

                        if grupos:
                            resultado = True

                    elif filtro == '3':
                        interesse_query = Q(interesse__icontains=item, ativo=True)
                        interesses = InteresseModel.objects.filter(interesse_query)

                        if interesses:
                            resultado = True

                    elif filtro == '4':
                        evento_query = Q(titulo__icontains=item, ativo=True)
                        eventos = EventoModel.objects.filter(evento_query)

                        if eventos:
                            resultado = True

                    elif filtro == '5':
                        postagem_query = Q(titulo__icontains=item, ativo=True)
                        postagens_grupos = PostagemGrupoModel.objects.filter(postagem_query)
                        postagens_eventos = PostagemEventoModel.objects.filter(postagem_query)

                        if postagens_eventos or postagens_grupos:
                            resultado = True

                elif not request.GET.get('f') or request.GET.get('f') == '0':
                    perfil_query = Q(usuario__full_name__icontains=item)
                    grupo_query = Q(nome__icontains=item)
                    interesse_query = Q(interesse__icontains=item)
                    evento_query = Q(titulo__icontains=item)
                    postagem_query = Q(titulo__icontains=item)

                    perfis = PerfilModel.objects.filter(perfil_query)

                    if perfis:
                        for perfil in perfis:
                            perfis_dict[perfil] = ImagemModel.objects.get(perfil=perfil)

                    grupos = GrupoModel.objects.filter(grupo_query, ativo=True)
                    interesses = InteresseModel.objects.filter(interesse_query, ativo=True)
                    eventos = EventoModel.objects.filter(evento_query, ativo=True)
                    postagens_grupos = PostagemGrupoModel.objects.filter(postagem_query, ativo=True)
                    postagens_eventos = PostagemEventoModel.objects.filter(postagem_query, ativo=True)

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

    if request.method == 'POST':

        convites_amigos_post(request, 'conviteAmigoForm')
        convites_eventos_post(request, 'conviteEventoForm')
        convites_grupos_post(request, 'conviteGrupoForm')

        return HttpResponseRedirect('/search/?q='+request.GET.get('q'))

    perfil = PerfilModel.objects.get(usuario=request.user)

    args['convites_grupos'] = load_convites_grupos(request)
    args['convites_eventos'] = load_convites_eventos(request)
    args['convites_amigos'] = load_convites_amigos(perfil)
    args['pesquisa_form'] = pesquisa_form
    args['perfil'] = perfil
    args['foto'] = ImagemModel.objects.get(perfil__usuario=request.user, is_profile_image=True)

    return render(request, 'mainAcad/search.html', args)


def view_reportar_bug(request):
    args = {}

    if request.method == 'POST':
        bug_form = ContatoForm(data=request.POST)

        if bug_form.is_valid():
            print request.POST

    else:
        bug_form = ContatoForm()


    args['contato_form'] = bug_form

    return render(request, 'mainAcad/bugs.html', args)


def view_denuncia(request):
    args = {}

    if request.method == 'POST':
        report_form = ContatoForm(data=request.POST)

        if report_form.is_valid():
            print request.POST

    else:
        report_form = ContatoForm()

    args['contato_form'] = report_form

    return render(request, 'mainAcad/denuncia.html', args)


def view_fale_conosco(request):
    args = {}

    if request.method == 'POST':
        contato_form = ContatoForm(data=request.POST)

        if contato_form.is_valid():
            print request.POST

    else:
        contato_form = ContatoForm()


    args['contato_form'] = contato_form

    return render(request, 'mainAcad/contato.html', args)


def custom_404(request):
    return render(request, '404.html', {}, status=404)


def custom_500(request):
    return render(request, '500.html', {}, status=500)