# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universidades', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universidademodel',
            name='nome',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='universidademodel',
            name='sigla',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
    ]
