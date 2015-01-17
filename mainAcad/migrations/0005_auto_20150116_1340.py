# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainAcad', '0004_auto_20150116_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConviteAmigoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 40, 12, 205000, tzinfo=utc))),
                ('ativo', models.BooleanField(default=True)),
                ('amigo', models.ForeignKey(related_name='amigo_convite', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(related_name='usuario_convite', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': ('contive (Amigo)',),
                'verbose_name_plural': ('contives (Amigo)',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='amigomodel',
            name='ativo',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='amigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 40, 12, 195000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 40, 12, 195000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
