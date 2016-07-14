# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import shuup.campaigns.models.cart_conditions


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsinbasketcondition',
            name='operator',
            field=enumfields.fields.EnumIntegerField(default=1, enum=shuup.campaigns.models.cart_conditions.ComparisonOperator, verbose_name='operator'),
        ),
    ]
