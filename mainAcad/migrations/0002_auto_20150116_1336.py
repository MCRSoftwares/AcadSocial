# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainAcad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmigoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amigo', models.ForeignKey(related_name='amigo', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 36, 0, 821000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
