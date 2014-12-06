# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição dos modelos relacionados à aplicação de contas (cadastro/login).
    Inclui os modelos: PerfilModel, UsuarioModel e UsuarioManager.
"""

from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from universidades.models import UniversidadeModel, CursoModel


class UsuarioManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        now = timezone.now()

        if not email:
            # TODO criar mensagem de erro para caso o e-mail não seja definido
            raise ValueError('')

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

    active_help_text = _('Designates whether this user should be treated as active.'
                         'Unselect this instead of deleting accounts.')

    staff_help_text = _('Designates whether the user can log into this admin site.')

    # Atributos do modelo

    uid = models.AutoField(_('user ID'), primary_key=True)
    email = models.EmailField(_('email'), max_length=200, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=128, blank=True)
    last_name = models.CharField(_('last name'), max_length=128, blank=True)

    is_active = models.BooleanField(_('active'), default=False, help_text=active_help_text)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=staff_help_text)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UsuarioManager()

    def get_absolute_url(self):
        # TODO definir uma URL real para este método
        return "/users/%s" % urlquote(self.uid)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')


class PerfilModel(models.Model):

    usuario = models.OneToOneField(UsuarioModel)
    foto = models.ImageField(_('picture'), upload_to='imagens/perfil/', default='imagens/perfil/default.jpg')
    data_nascimento = models.DateField(_('birth date'))
    universidade = models.ForeignKey(UniversidadeModel)
    curso = models.ForeignKey(CursoModel)
    chave_ativacao = models.CharField(_('activation key'), max_length=40, blank=True)

    def __unicode__(self):
        return self.usuario.email

    class Meta:
        verbose_name = _('perfil')
        verbose_name_plural = _('perfils')
