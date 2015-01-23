# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0004_auto_20150121_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarioeventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 857000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comentariogrupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 856000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteeventomodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 853000, tzinfo=utc), verbose_name='data de envio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convitegrupomodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 853000, tzinfo=utc), verbose_name='data de envio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 851000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 850000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 848000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interessemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 849000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membromodel',
            name='data_entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 851000, tzinfo=utc), verbose_name='data de entrada'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participaeventomodel',
            name='data_participacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 852000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postagemeventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 855000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postagemgrupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 854000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 13, 9, 4, 849000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
