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
        migrations.RemoveField(
            model_name='comentarioeventomodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='comentariogrupomodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='conviteeventomodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='convitegrupomodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='eventomodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='grupointeressemodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='membromodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='participaeventomodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='postagemeventomodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='usuariointeressemodel',
            name='id',
        ),
        migrations.AddField(
            model_name='comentarioeventomodel',
            name='cid',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comentariogrupomodel',
            name='cid',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conviteeventomodel',
            name='cid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='convitegrupomodel',
            name='cid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventomodel',
            name='eid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupointeressemodel',
            name='iid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membromodel',
            name='mid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participaeventomodel',
            name='eid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postagemeventomodel',
            name='pid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuariointeressemodel',
            name='iid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comentarioeventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 778000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comentariogrupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 777000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteeventomodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 775000, tzinfo=utc), verbose_name='data de envio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convitegrupomodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 774000, tzinfo=utc), verbose_name='data de envio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 772000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 771000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 769000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interessemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 770000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membromodel',
            name='data_entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 772000, tzinfo=utc), verbose_name='data de entrada'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participaeventomodel',
            name='data_participacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 773000, tzinfo=utc), verbose_name='data de participa\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postagemeventomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 776000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postagemgrupomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 775000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariointeressemodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 13, 57, 33, 770000, tzinfo=utc), verbose_name='data de cria\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
