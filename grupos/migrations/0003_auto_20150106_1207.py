# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grupos', '0002_auto_20150105_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConviteEventoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_envio', models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 487000, tzinfo=utc))),
                ('ativo', models.BooleanField(default=True)),
                ('aceito', models.BooleanField(default=False)),
                ('convidado', models.ForeignKey(related_name='evento_convidado', to=settings.AUTH_USER_MODEL)),
                ('evento', models.ForeignKey(to='grupos.EventoModel')),
                ('usuario', models.ForeignKey(related_name='evento_criador_convite', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_envio', models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 487000, tzinfo=utc))),
                ('ativo', models.BooleanField(default=True)),
                ('aceito', models.BooleanField(default=False)),
                ('convidado', models.ForeignKey(related_name='grupo_convidado', to=settings.AUTH_USER_MODEL)),
                ('grupo', models.ForeignKey(to='grupos.GrupoModel')),
                ('usuario', models.ForeignKey(related_name='grupo_criador_convite', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'convite (Grupo)',
                'verbose_name_plural': 'convites (Grupo)',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 485000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 484000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 483000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interessemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 482000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membromodel',
            name='data_entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 485000, tzinfo=utc), verbose_name='data de entrada'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participaeventomodel',
            name='data_participacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 486000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 15, 7, 36, 483000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
