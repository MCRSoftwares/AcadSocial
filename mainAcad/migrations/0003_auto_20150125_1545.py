# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0002_auto_20150122_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 168000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteamigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 169000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 18, 45, 34, 167000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='thumbnail',
            field=models.ImageField(default=b'imagens/perfil/default_thumbnail45.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='thumbnail_home',
            field=models.ImageField(default=b'imagens/perfil/default_thumbnail68.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='thumbnail_perfil',
            field=models.ImageField(default=b'imagens/perfil/default_thumbnail120.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail'),
            preserve_default=True,
        ),
    ]
