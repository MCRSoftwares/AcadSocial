# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição dos modelos da relação universidade-curso
    Inclui os modelos: UniversidadeModel, CursoModel.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UniversidadeModel(models.Model):
    sigla = models.CharField(max_length=20)
    nome = models.CharField(max_length=256)
    campus = models.CharField(max_length=128)

    def __unicode__(self):
        return self.sigla + ' (' + self.campus + ')'

    class Meta:
        verbose_name = _('universidade')
        verbose_name_plural = _('universidades')


class CursoModel(models.Model):
    nome = models.CharField(max_length=200)
    universidade = models.ForeignKey(UniversidadeModel)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _('curso')
        verbose_name_plural = _('cursos')