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
from mainAcad.methods import converter_para_jpg, gerar_thumbnail
from mainAcad.constants import DEFAULT_PICTURE
from PIL import Image


class ImagemModel(models.Model):

    active_help_text = _('Designates whether this image should be treated as active. '
                         'Unselect this instead of deleting images.')

    profile_help_text = _('Designates whether this image should be treated as a profile picture. '
                          'Unselect this instead of deleting the profile image.')

    imagem = models.ImageField(_('Image'), upload_to='imagens', default=DEFAULT_PICTURE)
    thumbnail_perfil = models.ImageField(_('Thumbnail'), upload_to='imagens/thumbnails/', default=DEFAULT_PICTURE)
    thumbnail_home = models.ImageField(_('Thumbnail'), upload_to='imagens/thumbnails/', default=DEFAULT_PICTURE)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to='imagens/thumbnails/', default=DEFAULT_PICTURE)
    perfil = models.ForeignKey(PerfilModel)
    data_envio = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True, help_text=active_help_text)
    is_profile_image = models.BooleanField(default=False, help_text=profile_help_text)

    def __unicode__(self):
        return str(self.imagem)

    def save(self, *args, **kwargs):

        imagem_path = '/imagens/'

        if self.imagem.name != DEFAULT_PICTURE:
            self.imagem = converter_para_jpg(self.imagem, imagem_path)
            temp_imagem = self.imagem

            imagem = Image.open(temp_imagem)
            self.thumbnail_perfil = gerar_thumbnail(imagem, temp_imagem, '_thumbnail120', (120, 120))
            self.thumbnail_home = gerar_thumbnail(imagem, temp_imagem, '_thumbnail68', (68, 68))
            self.thumbnail = gerar_thumbnail(imagem, temp_imagem, '_thumbnail45', (45, 45))

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