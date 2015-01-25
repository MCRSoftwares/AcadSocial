# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0008_auto_20150124_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarioeventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 179000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comentariogrupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 178000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteeventomodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 176000, tzinfo=utc), verbose_name='data de envio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convitegrupomodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 175000, tzinfo=utc), verbose_name='data de envio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 174000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='t\xedtulo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 172000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 170000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='nome',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interessemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 171000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membromodel',
            name='data_entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 173000, tzinfo=utc), verbose_name='data de entrada'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participaeventomodel',
            name='data_participacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 174000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postagemeventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 178000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postagemgrupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 177000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 171000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
