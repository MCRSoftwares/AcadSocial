# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universidades', '0002_auto_20150118_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='universidademodel',
            name='campus',
            field=models.CharField(default='Recife', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='universidademodel',
            name='sigla',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
