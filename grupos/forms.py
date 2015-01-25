# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição dos formulários relacionados à aplicação de grupos e eventos.
"""

from django import forms
from datetime import datetime
from grupos.errors import erro_interesse, erro_grupo, erro_evento
from contas.models import UsuarioModel
from grupos.models import ComentarioGrupoModel, InteresseModel, GrupoModel, PostagemGrupoModel
from grupos.models import ComentarioEventoModel, PostagemEventoModel, EventoModel


class ComentarioGrupoForm(forms.ModelForm):

    class Meta:
        model = ComentarioGrupoModel
        fields = ()


class ComentarioEventoForm(forms.ModelForm):

    class Meta:
        model = ComentarioEventoModel
        fields = ()


class InteresseSearchForm(forms.ModelForm):

    pesquisa_attrs = {
        'placeholder': 'Criar/Pesquisar Interesses...',
        'class': 'form-control search-bar-interesse',
        'id': 'interesseQry',
        'autocomplete': 'off',
    }

    iq = forms.CharField(max_length=64, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = InteresseModel
        fields = ('iq', )


class AdicionarInteresseForm(forms.ModelForm):

    interesse_attrs = {
        'id': 'interesseField',
    }

    criarInteresse = forms.CharField(max_length=64, widget=forms.HiddenInput(attrs=interesse_attrs))

    def clean(self):
        interesse = self.cleaned_data.get('criarInteresse')
        interesse = ' '.join(unicode(interesse).split())

        if not interesse or not ''.join(unicode(interesse).split()):
            raise forms.ValidationError(erro_interesse['interesse_invalido'], code='interesse_invalido')

        if unicode(interesse).startswith(' '):
            interesse = interesse[1:]

        try:
            InteresseModel.objects.get(interesse__iexact=interesse)

            raise forms.ValidationError(erro_interesse['interesse_ja_existente'], code='interesse_ja_existente')
        except InteresseModel.DoesNotExist:
            return self.cleaned_data

    class Meta:
        model = InteresseModel
        fields = ('criarInteresse', )


class GrupoSearchForm(forms.ModelForm):

    pesquisa_attrs = {
        'placeholder': 'Criar/Pesquisar Grupos...',
        'class': 'form-control search-bar-interesse',
        'id': 'grupoQry',
        'autocomplete': 'off',
    }

    gq = forms.CharField(max_length=64, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = GrupoModel
        fields = ('gq', )


class AdicionarGrupoForm(forms.ModelForm):

    grupo_attrs = {
        'id': 'grupoField'
    }

    criarGrupo = forms.CharField(max_length=64, widget=forms.HiddenInput(attrs=grupo_attrs))

    def clean(self):
        grupo = self.cleaned_data.get('criarGrupo')
        grupo = ' '.join(unicode(grupo).split())

        if not grupo or not ''.join(unicode(grupo).split()):
            raise forms.ValidationError(erro_grupo['grupo_invalido'], code='grupo_invalido')

        if unicode(grupo).startswith(' '):
            grupo = grupo[1:]

        try:
            GrupoModel.objects.get(nome__iexact=grupo)

            raise forms.ValidationError(erro_grupo['grupo_ja_existente'], code='grupo_ja_existente')
        except GrupoModel.DoesNotExist:
            return self.cleaned_data

    class Meta:
        model = GrupoModel
        fields = ('criarGrupo', )


class PostagemGrupoForm(forms.ModelForm):

    titulo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Título...',
    }

    conteudo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Conteúdo...',
        'maxlength': '256',
        'rows': '1',
    }

    titulo = forms.CharField(max_length=32, widget=forms.TextInput(attrs=titulo_attrs), required=True)
    conteudo = forms.CharField(widget=forms.Textarea(attrs=conteudo_attrs), required=True)

    class Meta:
        model = PostagemGrupoModel
        fields = ('titulo', 'conteudo', )


class PostagemEventoForm(forms.ModelForm):

    titulo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Título...',
    }

    conteudo_attrs = {
        'class': 'form-control form-panel',
        'placeholder': u'Conteúdo...',
        'maxlength': '256',
        'rows': '1',
    }

    titulo = forms.CharField(max_length=32, widget=forms.TextInput(attrs=titulo_attrs), required=True)
    conteudo = forms.CharField(widget=forms.Textarea(attrs=conteudo_attrs), required=True)

    class Meta:
        model = PostagemEventoModel
        fields = ('titulo', 'conteudo', )


class MembroSearchForm(forms.ModelForm):

    pesquisa_attrs = {
        'placeholder': 'Pesquisar Usuários...',
        'class': 'form-control search-bar-interesse',
        'id': 'usuarioQry',
        'autocomplete': 'off',
    }

    aq = forms.CharField(max_length=64, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = GrupoModel
        fields = ('aq', )


class EditarGrupoForm(forms.ModelForm):

    nome_attrs = {
        'class': 'form-control',
        'id': 'nomeGrupoEditar',
    }

    descricao_attrs = {
        'class': 'form-control',
        'id': 'descricaoGrupoEditar',
        'maxlength': '1024',
        'rows': '2',
    }

    nome = forms.CharField(widget=forms.TextInput(attrs=nome_attrs), max_length=100, required=True)
    descricao = forms.CharField(widget=forms.Textarea(attrs=descricao_attrs), max_length=1024, required=True)

    class Meta:
        model = GrupoModel
        fields = ('nome', 'descricao', )


class AdminGrupoForm(forms.ModelForm):

    membro_attrs = {
        'class': 'form-control'
    }

    membro = forms.ModelChoiceField(queryset=None,
                                    empty_label='Selecione o e-mail de um membro',
                                    widget=forms.Select(attrs=membro_attrs))

    class Meta:
        model = UsuarioModel
        fields = ('membro', )


class EventoForm(forms.ModelForm):

    titulo_attrs = {
        'class': 'form-control',
        'id': 'eventoTitulo'
    }

    descricao_attrs = {
        'class': 'form-control',
        'maxlength': '256',
        'id': 'eventoDesc',
        'rows': '2',
    }

    dia_attrs = {
        'class': 'form-control',
        'id': 'eventoDia',
    }

    mes_attrs = {
        'class': 'form-control',
        'id': 'eventoMes',
    }

    ano_attrs = {
        'class': 'form-control',
        'id': 'eventoAno',
    }

    hora_attrs = {
        'class': 'form-control',
        'id': 'eventoHora',
    }

    minutos_attrs = {
        'class': 'form-control',
        'id': 'eventoMinutos',
    }

    local_attrs = {
        'class': 'form-control',
        'id': 'eventoLocal',
    }

    dia_list = [(x, str(x)) for x in range(1, 32)]
    dia_list.insert(0, (0, 'Dia'))

    mes_list = [(x, str(x)) for x in range(1, 13)]
    mes_list.insert(0, (0, 'Mês'))

    ano_list = [(x, str(x)) for x in range(datetime.today().year, datetime.today().year + 2)]
    ano_list.insert(0, (0, 'Ano'))

    hora_list = [(x, str(x)) for x in range(0, 24)]
    hora_list.insert(0, (0, 'Hora'))

    minutos_list = [(x * 5, str(x * 5)) for x in range(0, 12)]
    minutos_list.insert(0, (0, 'Minutos'))

    dia = forms.ChoiceField(choices=dia_list, widget=forms.Select(dia_attrs))
    mes = forms.ChoiceField(choices=mes_list, widget=forms.Select(mes_attrs))
    ano = forms.ChoiceField(choices=ano_list, widget=forms.Select(ano_attrs))
    hora = forms.ChoiceField(choices=hora_list, widget=forms.Select(hora_attrs))
    minutos = forms.ChoiceField(choices=minutos_list, widget=forms.Select(minutos_attrs))
    titulo = forms.CharField(max_length=100, widget=forms.TextInput(attrs=titulo_attrs))
    descricao = forms.CharField(max_length=256, widget=forms.Textarea(attrs=descricao_attrs))
    local_evento = forms.CharField(max_length=140, widget=forms.TextInput(attrs=local_attrs))

    def clean(self):

        dia = self.cleaned_data.get('dia')
        mes = self.cleaned_data.get('mes')
        ano = self.cleaned_data.get('ano')
        hora = self.cleaned_data.get('hora')
        minutos = self.cleaned_data.get('minutos')

        data_str = str(dia) + '-' + str(mes) + '-' + str(ano) + ' ' + str(hora) + ':' + str(minutos)

        try:
            datetime.strptime(data_str, '%d-%m-%Y %H:%M')
        except ValueError:
            raise forms.ValidationError(erro_evento['data_invalida'], code='data_invalida')

        return self.cleaned_data

    class Meta:
        model = EventoModel
        fields = ('dia', 'mes', 'ano', 'hora', 'minutos', 'local_evento', 'titulo', 'descricao',)