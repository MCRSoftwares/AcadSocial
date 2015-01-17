# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_auto_20150116_1409'),
        ('mainAcad', '0005_auto_20150116_1340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amigomodel',
            options={'verbose_name': 'amigo', 'verbose_name_plural': 'amigos'},
        ),
        migrations.AlterModelOptions(
            name='conviteamigomodel',
            options={'verbose_name': 'convite (Amigo)', 'verbose_name_plural': 'convites (Amigo)'},
        ),
        migrations.RemoveField(
            model_name='amigomodel',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='conviteamigomodel',
            name='usuario',
        ),
        migrations.AddField(
            model_name='amigomodel',
            name='perfil',
            field=models.ForeignKey(related_name='perfil', default=0, to='contas.PerfilModel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conviteamigomodel',
            name='perfil',
            field=models.ForeignKey(related_name='perfil_convite', default=0, to='contas.PerfilModel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='amigomodel',
            name='amigo',
            field=models.ForeignKey(related_name='amigo', to='contas.PerfilModel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='amigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 17, 9, 29, 8000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteamigomodel',
            name='amigo',
            field=models.ForeignKey(related_name='amigo_convite', to='contas.PerfilModel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteamigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 17, 9, 29, 9000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 17, 9, 29, 7000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
