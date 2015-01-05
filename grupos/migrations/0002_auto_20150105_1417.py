# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventomodel',
            options={'verbose_name': 'evento', 'verbose_name_plural': 'eventos'},
        ),
        migrations.AlterModelOptions(
            name='grupomodel',
            options={'verbose_name': 'grupo', 'verbose_name_plural': 'grupos'},
        ),
        migrations.AlterModelOptions(
            name='membromodel',
            options={'verbose_name': 'membro', 'verbose_name_plural': 'membros'},
        ),
        migrations.AlterModelOptions(
            name='participaeventomodel',
            options={'verbose_name': 'participa\xe7\xe3o (Evento)', 'verbose_name_plural': 'participa\xe7\xf5es (Evento)'},
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 17, 42, 670000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='descricao',
            field=models.TextField(max_length=1024, verbose_name='Descri\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 17, 42, 669000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='descricao',
            field=models.TextField(max_length=1024, verbose_name='descri\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membromodel',
            name='data_entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 17, 42, 669000, tzinfo=utc), verbose_name='data de entrada'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participaeventomodel',
            name='data_participacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 17, 17, 42, 671000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
