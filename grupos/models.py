# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v006a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF004, RF005, RF007, RF006
Caso(s) de Uso: DVA001, DVA002, DVA006, DVA007

Descrição:
    Definição dos modelos relacionados à aplicação de grupos e eventos.
    Inclui os modelos: GrupoModel, EventoModel, MembroModel, ParticipaEventoModel,
                       InteresseModel, UsuarioInteresseModel, GrupoInteresseModel,
                       ConviteGrupoModel, ConviteEventoModel, PostagemGrupoModel,
                       PostagemEventoModel, ComentarioGrupoModel, ComentarioEventoModel.
"""

from django.db import models
from contas.models import UsuarioModel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class GrupoModel(models.Model):
    gid = models.AutoField(_('grupo ID'), primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(_(u'descrição'), max_length=1024)
    criado_por = models.ForeignKey(UsuarioModel, related_name='criador_grupo')
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nome + ' (' + unicode(self.criado_por) + ')'

    class Meta:
        verbose_name = _('grupo')
        verbose_name_plural = _('grupos')


class InteresseModel(models.Model):
    iid = models.AutoField(_('interesse ID'), primary_key=True)
    interesse = models.CharField(max_length=96)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())
    criado_por = models.ForeignKey(UsuarioModel)
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.interesse

    class Meta:
        verbose_name = _(u'interesse')
        verbose_name_plural = _(u'interesses')


class UsuarioInteresseModel(models.Model):
    interesse = models.ForeignKey(InteresseModel)
    usuario = models.ForeignKey(UsuarioModel)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())
    ativo = models.BooleanField(default=True)
    iid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return unicode(self.interesse) + ' - ' + unicode(self.usuario)

    class Meta:
        verbose_name = _(u'relação Usuário-Interesse')
        verbose_name_plural = _(u'relações Usuário-Interesse')


class GrupoInteresseModel(models.Model):
    interesse = models.ForeignKey(InteresseModel)
    grupo = models.ForeignKey(GrupoModel)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())
    iid = models.AutoField(primary_key=True)
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.interesse) + ' - ' + unicode(self.grupo)

    class Meta:
        verbose_name = _(u'relação Grupo-Interesse')
        verbose_name_plural = _(u'relações Grupo-Interesse')


class MembroModel(models.Model):
    usuario = models.ForeignKey(UsuarioModel)
    grupo = models.ForeignKey(GrupoModel)
    data_entrada = models.DateTimeField(_('data de entrada'), default=timezone.now())
    is_admin = models.BooleanField(_('administrador'), default=False)
    mid = models.AutoField(primary_key=True)
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.grupo) + ' - ' + unicode(self.usuario)

    class Meta:
        verbose_name = _('membro')
        verbose_name_plural = _('membros')


class EventoModel(models.Model):
    titulo = models.CharField(_(u'título'), max_length=100)
    descricao = models.TextField(_(u'descrição'), max_length=256)
    grupo = models.ForeignKey(GrupoModel)
    data_criacao = models.DateTimeField(_(u'data de criação'), default=timezone.now())
    data_evento = models.DateTimeField(_('data do evento'))
    local_evento = models.CharField(_('local do evento'), max_length=140)
    criado_por = models.ForeignKey(UsuarioModel)
    eid = models.AutoField(primary_key=True)
    ativo = models.BooleanField(default=True)
    cancelado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo + ' (' + unicode(self.criado_por) + ')'

    class Meta:
        verbose_name = _('evento')
        verbose_name_plural = _('eventos')


class ParticipaEventoModel(models.Model):
    evento = models.ForeignKey(EventoModel)
    usuario = models.ForeignKey(UsuarioModel)
    data_participacao = models.DateTimeField(_(u'data de participação'), default=timezone.now())
    eid = models.AutoField(primary_key=True)
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.evento) + ' - ' + unicode(self.usuario)

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
    cid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return unicode(self.grupo) + ' (' + unicode(self.usuario) + ': ' + unicode(self.convidado) + ')'

    class Meta:
        verbose_name = _('convite (Grupo)')
        verbose_name_plural = _('convites (Grupo)')


class ConviteEventoModel(models.Model):
    usuario = models.ForeignKey(UsuarioModel, related_name='evento_criador_convite')
    convidado = models.ForeignKey(UsuarioModel, related_name='evento_convidado')
    data_envio = models.DateTimeField(_('data de envio'), default=timezone.now())
    evento = models.ForeignKey(EventoModel)
    grupo = models.ForeignKey(GrupoModel)
    ativo = models.BooleanField(default=True)
    aceito = models.BooleanField(default=False)
    cid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return unicode(self.evento) + ' (' + unicode(self.usuario) + ': ' + unicode(self.convidado) + ')'

    class Meta:
        verbose_name = _('convite (Evento)')
        verbose_name_plural = _('convites (Evento)')


class PostagemGrupoModel(models.Model):
    criado_por = models.ForeignKey(UsuarioModel, related_name='grupo_criador_postagem')
    titulo = models.CharField(_(u'título'), max_length=64)
    conteudo = models.TextField(_(u'conteúdo'), max_length=2048)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(default=timezone.now())
    grupo = models.ForeignKey(GrupoModel)
    pid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return unicode(self.grupo) + ' (' + unicode(self.criado_por) + ': ' + unicode(self.data_criacao) + ')'

    class Meta:
        verbose_name = _('postagem (Grupo)')
        verbose_name_plural = _('postagens (Grupo)')


class PostagemEventoModel(models.Model):
    criado_por = models.ForeignKey(UsuarioModel, related_name='evento_criador_postagem')
    titulo = models.CharField(_(u'título'), max_length=64)
    conteudo = models.TextField(_(u'conteúdo'), max_length=2048)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(default=timezone.now())
    grupo = models.ForeignKey(GrupoModel)
    evento = models.ForeignKey(EventoModel)
    pid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return unicode(self.evento) + ' (' + unicode(self.criado_por) + ': ' + unicode(self.data_criacao) + ')'

    class Meta:
        verbose_name = _('postagem (Evento)')
        verbose_name_plural = _('postagens (Evento)')


class ComentarioGrupoModel(models.Model):
    criado_por = models.ForeignKey(UsuarioModel)
    conteudo = models.TextField(_(u'conteúdo'))
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(default=timezone.now())
    postagem = models.ForeignKey(PostagemGrupoModel)
    cid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return unicode(self.postagem) + ' (' + unicode(self.criado_por) + ': ' + unicode(self.data_criacao) + ')'

    class Meta:
        verbose_name = _(u'comentário (Grupo)')
        verbose_name_plural = _(u'comentários (Grupo)')


class ComentarioEventoModel(models.Model):
    criado_por = models.ForeignKey(UsuarioModel)
    conteudo = models.TextField(_(u'conteúdo'))
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(default=timezone.now())
    postagem = models.ForeignKey(PostagemEventoModel)
    cid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return unicode(self.postagem) + ' (' + unicode(self.criado_por) + ': ' + unicode(self.data_criacao) + ')'

    class Meta:
        verbose_name = _(u'comentário (Evento)')
        verbose_name_plural = _(u'comentários (Evento)')
