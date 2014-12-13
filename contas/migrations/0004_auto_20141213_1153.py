# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_auto_20141213_1151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfilmodel',
            old_name='amizades',
            new_name='contatos',
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 14, 53, 12, 583000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 14, 53, 12, 583000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
