# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição dos modelos relacionadas à aplicação principal.
"""

from django.db import models
from contas.models import PerfilModel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mainAcad.methods import gerar_thumbnail, upload_image_as, upload_with_boto
from mainAcad.constants import DEFAULT_PICTURE, DEFAULT_PICTURE_THUMBNAIL
from mainAcad.constants import DEFAULT_PICTURE_THUMBNAIL_HOME, DEFAULT_PICTURE_THUMBNAIL_PERFIL
from PIL import Image


class ImagemModel(models.Model):

    active_help_text = _('Designates whether this image should be treated as active. '
                         'Unselect this instead of deleting images.')

    profile_help_text = _('Designates whether this image should be treated as a profile picture. '
                          'Unselect this instead of deleting the profile image.')

    imagem = models.ImageField(_('Image'), upload_to=upload_image_as, default=DEFAULT_PICTURE)
    thumbnail_perfil = models.ImageField(_('Thumbnail120'), default=DEFAULT_PICTURE_THUMBNAIL_PERFIL)
    thumbnail_home = models.ImageField(_('Thumbnail68'), default=DEFAULT_PICTURE_THUMBNAIL_HOME)
    thumbnail = models.ImageField(_('Thumbnail45'), default=DEFAULT_PICTURE_THUMBNAIL)

    perfil = models.ForeignKey(PerfilModel)
    data_envio = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True, help_text=active_help_text)
    is_profile_image = models.BooleanField(default=False, help_text=profile_help_text)

    def __unicode__(self):
        return str(self.imagem)

    def save(self, *args, **kwargs):
        super(ImagemModel, self).save(*args, **kwargs)
        temp_imagem = Image.open(self.imagem)

        self.thumbnail_perfil = gerar_thumbnail(temp_imagem, self.imagem.name, '-120', (120, 120))
        self.thumbnail_home = gerar_thumbnail(temp_imagem, self.imagem.name, '-68', (68, 68))
        self.thumbnail = gerar_thumbnail(temp_imagem, self.imagem.name, '-45', (45, 45))

        upload_with_boto(self.thumbnail_perfil.name, self.thumbnail_home.name, self.thumbnail.name)
        super(ImagemModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('imagem')
        verbose_name_plural = _('imagens')


class AmigoModel(models.Model):
    perfil = models.ForeignKey(PerfilModel, related_name='perfil')
    amigo = models.ForeignKey(PerfilModel, related_name='amigo')
    data_criacao = models.DateTimeField(default=timezone.now())
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.perfil.usuario.email + u' é amigo de ' + self.amigo.usuario.email

    class Meta:
        verbose_name = _('amigo')
        verbose_name_plural = _('amigos')


class ConviteAmigoModel(models.Model):
    perfil = models.ForeignKey(PerfilModel, related_name='perfil_convite')
    amigo = models.ForeignKey(PerfilModel, related_name='amigo_convite')
    data_criacao = models.DateTimeField(default=timezone.now())
    ativo = models.BooleanField(default=True)
    cid = models.AutoField(primary_key=True)

    def __unicode__(self):
        return self.perfil.usuario.email + ' quer ser amigo de ' + self.amigo.usuario.email

    class Meta:
        verbose_name = _('convite (Amigo)')
        verbose_name_plural = _('convites (Amigo)')