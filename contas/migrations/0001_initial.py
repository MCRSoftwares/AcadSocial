# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('universidades', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioModel',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uid', models.AutoField(serialize=False, verbose_name='user ID', primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=200, verbose_name='email', db_index=True)),
                ('first_name', models.CharField(max_length=128, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=128, verbose_name='last name', blank=True)),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active.Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PerfilModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foto', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/perfil/', verbose_name='picture')),
                ('data_nascimento', models.DateField(verbose_name='birth date')),
                ('chave_ativacao', models.CharField(max_length=40, verbose_name='activation key', blank=True)),
                ('curso', models.ForeignKey(to='universidades.CursoModel')),
                ('universidade', models.ForeignKey(to='universidades.UniversidadeModel')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfils',
            },
            bases=(models.Model,),
        ),
    ]
