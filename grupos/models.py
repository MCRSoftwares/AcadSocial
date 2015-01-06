# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF004, RF005, RF007, RF006
Caso(s) de Uso: DVA001, DVA002, DVA006, DVA007

Descrição:
    Definição dos modelos relacionados à aplicação de grupos e eventos.
    Inclui os modelos: GrupoModel, EventoModel, MembroModel, ParticipaEventoModel,
                       InteresseModel, UsuarioInteresseModel, GrupoInteresseModel,
                       ConviteGrupoModel, ConviteEventoModel.
"""

from django.db import models
from contas.models import UsuarioModel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class InteresseModel(models.Model):
    iid = models.AutoField(_('interesse ID'), primary_key=True)
    interesse = models.CharField(max_length=96)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())

    def __unicode__(self):
        return self.interesse

    class Meta:
        verbose_name = _(u'interesse')
        verbose_name_plural = _(u'interesses')


class UsuarioInteresseModel(models.Model):
    interesse = models.ForeignKey(InteresseModel)
    usuario = models.ForeignKey(UsuarioModel)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())

    def __unicode__(self):
        return str(self.interesse) + ' - ' + str(self.usuario)

    class Meta:
        verbose_name = _(u'relação Usuário-Interesse')
        verbose_name_plural = _(u'relações Usuário-Interesse')


class GrupoModel(models.Model):
    gid = models.AutoField(_('grupo ID'), primary_key=True)
    nome = models.CharField(max_length=128)
    descricao = models.TextField(_(u'descrição'), max_length=1024)
    criado_por = models.ForeignKey(UsuarioModel)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())

    def __unicode__(self):
        return self.nome + ' (' + str(self.criado_por) + ')'

    class Meta:
        verbose_name = _('grupo')
        verbose_name_plural = _('grupos')


class GrupoInteresseModel(models.Model):
    interesse = models.ForeignKey(InteresseModel)
    grupo = models.ForeignKey(GrupoModel)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())

    def __unicode__(self):
        return str(self.interesse) + ' - ' + str(self.grupo)

    class Meta:
        verbose_name = _(u'relação Grupo-Interesse')
        verbose_name_plural = _(u'relações Grupo-Interesse')


class MembroModel(models.Model):
    usuario = models.ForeignKey(UsuarioModel)
    grupo = models.ForeignKey(GrupoModel)
    data_entrada = models.DateTimeField(_('data de entrada'), default=timezone.now())
    is_admin = models.BooleanField(_('administrador'), default=False)

    def __unicode__(self):
        return str(self.grupo) + ' - ' + str(self.usuario)

    class Meta:
        verbose_name = _('membro')
        verbose_name_plural = _('membros')


class EventoModel(models.Model):
    titulo = models.CharField(_(u'título'), max_length=128)
    descricao = models.TextField(_(u'descrição'), max_length=1024)
    grupo = models.ForeignKey(GrupoModel)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())
    data_evento = models.DateTimeField(_('data do evento'))
    criado_por = models.ForeignKey(UsuarioModel)

    def __unicode__(self):
        return self.titulo + ' (' + str(self.criado_por) + ')'

    class Meta:
        verbose_name = _('evento')
        verbose_name_plural = _('eventos')


class ParticipaEventoModel(models.Model):
    evento = models.ForeignKey(EventoModel)
    usuario = models.ForeignKey(UsuarioModel)
    data_participacao = models.DateTimeField(_(u'data de participação'), default=timezone.now())

    def __unicode__(self):
        return str(self.evento) + ' - ' + str(self.usuario)

    class Meta:
        verbose_name = _(u'relaçao Usuário-Evento')
        verbose_name_plural = _(u'relações Usuário-Evento')


class ConviteGrupoModel(models.Model):
    usuario = models.ForeignKey(UsuarioModel, related_name='grupo_criador_convite')
    convidado = models.ForeignKey(UsuarioModel, related_name='grupo_convidado')
    data_envio = models.DateTimeField(_('data de envio'), default=timezone.now())
    grupo = models.ForeignKey(GrupoModel)
    ativo = models.BooleanField(default=True)
    aceito = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.grupo) + ' (' + str(self.usuario) + ': ' + str(self.convidado) + ')'

    class Meta:
        verbose_name = _('convite (Grupo)')
        verbose_name_plural = _('convites (Grupo)')


class ConviteEventoModel(models.Model):
    usuario = models.ForeignKey(UsuarioModel, related_name='evento_criador_convite')
    convidado = models.ForeignKey(UsuarioModel, related_name='evento_convidado')
    data_envio = models.DateTimeField(_('data de envio'), default=timezone.now())
    evento = models.ForeignKey(EventoModel)
    ativo = models.BooleanField(default=True)
    aceito = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.evento) + ' (' + str(self.usuario) + ': ' + str(self.convidado) + ')'

    class Meta:
        verbose_name = _('convite (Evento)')
        verbose_name_plural = _('convites (Evento)')
