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
            name='ComentarioEventoModel',
            fields=[
                ('conteudo', models.TextField(verbose_name='conte\xfado')),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 510000, tzinfo=utc))),
                ('cid', models.AutoField(serialize=False, primary_key=True)),
                ('criado_por', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'coment\xe1rio (Evento)',
                'verbose_name_plural': 'coment\xe1rios (Evento)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ComentarioGrupoModel',
            fields=[
                ('conteudo', models.TextField(verbose_name='conte\xfado')),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 510000, tzinfo=utc))),
                ('cid', models.AutoField(serialize=False, primary_key=True)),
                ('criado_por', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'coment\xe1rio (Grupo)',
                'verbose_name_plural': 'coment\xe1rios (Grupo)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConviteEventoModel',
            fields=[
                ('data_envio', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 507000, tzinfo=utc), verbose_name='data de envio')),
                ('ativo', models.BooleanField(default=True)),
                ('aceito', models.BooleanField(default=False)),
                ('cid', models.AutoField(serialize=False, primary_key=True)),
                ('convidado', models.ForeignKey(related_name='evento_convidado', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'convite (Evento)',
                'verbose_name_plural': 'convites (Evento)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConviteGrupoModel',
            fields=[
                ('data_envio', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 507000, tzinfo=utc), verbose_name='data de envio')),
                ('ativo', models.BooleanField(default=True)),
                ('aceito', models.BooleanField(default=False)),
                ('cid', models.AutoField(serialize=False, primary_key=True)),
                ('convidado', models.ForeignKey(related_name='grupo_convidado', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'convite (Grupo)',
                'verbose_name_plural': 'convites (Grupo)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventoModel',
            fields=[
                ('titulo', models.CharField(max_length=128, verbose_name='t\xedtulo')),
                ('descricao', models.TextField(max_length=1024, verbose_name='descri\xe7\xe3o')),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 505000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('data_evento', models.DateTimeField(verbose_name='data do evento')),
                ('eid', models.AutoField(serialize=False, primary_key=True)),
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
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 504000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('iid', models.AutoField(serialize=False, primary_key=True)),
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
                ('gid', models.AutoField(serialize=False, verbose_name='grupo ID', primary_key=True)),
                ('nome', models.CharField(max_length=128)),
                ('descricao', models.TextField(max_length=1024, verbose_name='descri\xe7\xe3o')),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 502000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('criado_por', models.ForeignKey(related_name='criador_grupo', to=settings.AUTH_USER_MODEL)),
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
                ('iid', models.AutoField(serialize=False, verbose_name='interesse ID', primary_key=True)),
                ('interesse', models.CharField(max_length=96)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 503000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('criado_por', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('data_entrada', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 505000, tzinfo=utc), verbose_name='data de entrada')),
                ('is_admin', models.BooleanField(default=False, verbose_name='administrador')),
                ('mid', models.AutoField(serialize=False, primary_key=True)),
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
                ('data_participacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 506000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o')),
                ('eid', models.AutoField(serialize=False, primary_key=True)),
                ('evento', models.ForeignKey(to='grupos.EventoModel')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'rela\xe7ao Usu\xe1rio-Evento',
                'verbose_name_plural': 'rela\xe7\xf5es Usu\xe1rio-Evento',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostagemEventoModel',
            fields=[
                ('titulo', models.CharField(max_length=64, verbose_name='t\xedtulo')),
                ('conteudo', models.TextField(max_length=2048, verbose_name='conte\xfado')),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 509000, tzinfo=utc))),
                ('pid', models.AutoField(serialize=False, primary_key=True)),
                ('criado_por', models.ForeignKey(related_name='evento_criador_postagem', to=settings.AUTH_USER_MODEL)),
                ('evento', models.ForeignKey(to='grupos.EventoModel')),
                ('grupo', models.ForeignKey(to='grupos.GrupoModel')),
            ],
            options={
                'verbose_name': 'postagem (Evento)',
                'verbose_name_plural': 'postagens (Evento)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostagemGrupoModel',
            fields=[
                ('titulo', models.CharField(max_length=64, verbose_name='t\xedtulo')),
                ('conteudo', models.TextField(max_length=2048, verbose_name='conte\xfado')),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 508000, tzinfo=utc))),
                ('pid', models.AutoField(serialize=False, primary_key=True)),
                ('criado_por', models.ForeignKey(related_name='grupo_criador_postagem', to=settings.AUTH_USER_MODEL)),
                ('grupo', models.ForeignKey(to='grupos.GrupoModel')),
            ],
            options={
                'verbose_name': 'postagem (Grupo)',
                'verbose_name_plural': 'postagens (Grupo)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuarioInteresseModel',
            fields=[
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 49, 503000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o')),
                ('iid', models.AutoField(serialize=False, primary_key=True)),
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
        migrations.AddField(
            model_name='convitegrupomodel',
            name='grupo',
            field=models.ForeignKey(to='grupos.GrupoModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='convitegrupomodel',
            name='usuario',
            field=models.ForeignKey(related_name='grupo_criador_convite', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conviteeventomodel',
            name='evento',
            field=models.ForeignKey(to='grupos.EventoModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conviteeventomodel',
            name='usuario',
            field=models.ForeignKey(related_name='evento_criador_convite', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentariogrupomodel',
            name='postagem',
            field=models.ForeignKey(to='grupos.PostagemGrupoModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentarioeventomodel',
            name='postagem',
            field=models.ForeignKey(to='grupos.PostagemEventoModel'),
            preserve_default=True,
        ),
    ]
