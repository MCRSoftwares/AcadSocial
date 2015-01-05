# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=128, verbose_name='Descri\xe7\xe3o')),
                ('descricao', models.TextField(max_length=1024, verbose_name='Descri\xe7\xe3o')),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 19, 37, 28, 32000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('data_evento', models.DateTimeField(verbose_name='data do evento')),
                ('criado_por', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'evento',
                'verbose_name_plural': 'eventos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrupoInteresseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 19, 37, 28, 30000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
            ],
            options={
                'verbose_name': 'rela\xe7\xe3o Grupo-Interesse',
                'verbose_name_plural': 'rela\xe7\xf5es Grupo-Interesse',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrupoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=128)),
                ('descricao', models.TextField(max_length=1024, verbose_name='descri\xe7\xe3o')),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 19, 37, 28, 29000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('criado_por', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'grupo',
                'verbose_name_plural': 'grupos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InteresseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interesse', models.CharField(max_length=96)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 19, 37, 28, 28000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
            ],
            options={
                'verbose_name': 'interesse',
                'verbose_name_plural': 'interesses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MembroModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_entrada', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 19, 37, 28, 31000, tzinfo=utc), verbose_name='data de entrada')),
                ('is_admin', models.BooleanField(default=False, verbose_name='administrador')),
                ('grupo', models.ForeignKey(to='grupos.GrupoModel')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'membro',
                'verbose_name_plural': 'membros',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipaEventoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_participacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 19, 37, 28, 33000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o')),
                ('evento', models.ForeignKey(to='grupos.EventoModel')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'participa\xe7\xe3o (Evento)',
                'verbose_name_plural': 'participa\xe7\xf5es (Evento)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuarioInteresseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 19, 37, 28, 29000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('interesse', models.ForeignKey(to='grupos.InteresseModel')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'rela\xe7\xe3o Usu\xe1rio-Interesse',
                'verbose_name_plural': 'rela\xe7\xf5es Usu\xe1rio-Interesse',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='grupointeressemodel',
            name='grupo',
            field=models.ForeignKey(to='grupos.GrupoModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grupointeressemodel',
            name='interesse',
            field=models.ForeignKey(to='grupos.InteresseModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventomodel',
            name='grupo',
            field=models.ForeignKey(to='grupos.GrupoModel'),
            preserve_default=True,
        ),
    ]