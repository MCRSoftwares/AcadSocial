# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grupos', '0002_auto_20150105_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoInteresseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grupo', models.ForeignKey(to='grupos.GrupoModel')),
            ],
            options={
                'verbose_name': 'rela\xe7\xe3o Grupo-Interesse',
                'verbose_name_plural': 'rela\xe7\xf5es Grupo-Interesse',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InteresseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=96)),
            ],
            options={
                'verbose_name': 'interesse',
                'verbose_name_plural': 'interesses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuarioInteresseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            name='interesse',
            field=models.ForeignKey(to='grupos.InteresseModel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 31, 14, 453000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 31, 14, 451000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membromodel',
            name='data_entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 31, 14, 452000, tzinfo=utc), verbose_name='data de entrada'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participaeventomodel',
            name='data_participacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 31, 14, 454000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
