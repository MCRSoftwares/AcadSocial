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
                ('descricao', models.CharField(max_length=1024, verbose_name='Descri\xe7\xe3o')),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 13, 48, 760000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('data_evento', models.DateTimeField(verbose_name='data do evento')),
                ('criado_por', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrupoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=128)),
                ('descricao', models.CharField(max_length=1024, verbose_name='descri\xe7\xe3o')),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 13, 48, 759000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('criado_por', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MembroModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_entrada', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 13, 48, 760000, tzinfo=utc), verbose_name='data de entrada')),
                ('is_admin', models.BooleanField(default=False, verbose_name='administrador')),
                ('grupo', models.ForeignKey(to='grupos.GrupoModel')),
                ('membro', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipaEventoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_participacao', models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 13, 48, 761000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o')),
                ('evento', models.ForeignKey(to='grupos.EventoModel')),
                ('membro', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventomodel',
            name='grupo',
            field=models.ForeignKey(to='grupos.GrupoModel'),
            preserve_default=True,
        ),
    ]
