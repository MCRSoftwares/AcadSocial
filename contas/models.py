# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v005a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição dos modelos relacionados à aplicação de contas (cadastro/login).
    Inclui os modelos: PerfilModel, UsuarioModel e TokenModel.
"""

from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import timedelta
from universidades.models import UniversidadeModel, CursoModel
from django.template.defaultfilters import slugify
from contas.methods import selecionar_inicio_email


class UsuarioManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        now = timezone.now()

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, is_active=is_active,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)


class UsuarioModel(AbstractBaseUser, PermissionsMixin):

    """
    Substitui o modelo de Usuário original do django.
    Este fora criado para aceitar somente o e-mail como "username"
    """

    # Definição dos help_texts

    active_help_text = _('Designates whether this user should be treated as active. '
                         'Unselect this instead of deleting accounts.')

    staff_help_text = _('Designates whether the user can log into this admin site.')

    # Atributos do modelo

    uid = models.AutoField(_('user ID'), primary_key=True)
    email = models.EmailField(_('email'), max_length=200, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=128, blank=True)
    last_name = models.CharField(_('last name'), max_length=128, blank=True)
    full_name = models.CharField(_('full name'), max_length=256)
    is_active = models.BooleanField(_('active'), default=False, help_text=active_help_text)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=staff_help_text)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UsuarioManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        super(UsuarioModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')


class PerfilModel(models.Model):

    usuario = models.OneToOneField(UsuarioModel)
    data_nascimento = models.DateField(_('birth date'))
    universidade = models.ForeignKey(UniversidadeModel)
    curso = models.ForeignKey(CursoModel)

    perfil_link = models.CharField(_('profile link'), max_length=128, unique=True)

    def __unicode__(self):
        return self.usuario.email

    def save(self, *args, **kwargs):

        if self.usuario.email:
            self.perfil_link = slugify(self.get_short_email())

        super(PerfilModel, self).save(*args, **kwargs)

    def get_short_email(self):
        return selecionar_inicio_email(self.usuario.email)

    def get_absolute_url(self):
        return "/perfil/%s/%s" % (urlquote(slugify(self.universidade.sigla)), urlquote(self.perfil_link))

    class Meta:
        verbose_name = _('perfil')
        verbose_name_plural = _('perfis')


class TokenModel(models.Model):

    active_help_text = _('Designates whether this token should be treated as active. '
                         'An inactive token is a token that expired before being used. '
                         'Unselect this instead of deleting tokens.')

    valid_help_text = _('Designates whether this token should be treated as valid. '
                        'An invalid token cannot be accessed. '
                        'Unselect this instead of deleting tokens.')

    usuario = models.ForeignKey(UsuarioModel)
    tipo = models.CharField(max_length=128)
    token = models.CharField(_('token'), max_length=128, blank=True)
    data_request = models.DateTimeField(_('request date'), default=timezone.now())
    data_expiracao = models.DateTimeField(_('expiration date'), default=(timezone.now() + timedelta(days=1)))
    active = models.BooleanField(_('active'), default=True, help_text=active_help_text)
    valid = models.BooleanField(_('valid'), default=True, help_text=valid_help_text)

    def __unicode__(self):
        return self.token + '(active=' + str(self.active) + ', valid=' + str(self.valid) + ', type=' + self.tipo + ')'

    class Meta:
        verbose_name = _('token')
        verbose_name_plural = _('tokens')