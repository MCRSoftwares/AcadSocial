# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0008_auto_20141208_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(verbose_name='request date'),
            preserve_default=True,
        ),
    ]
