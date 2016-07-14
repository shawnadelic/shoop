# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shuup', '0002_rounding'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shuup_front', '0002_storedcart'),
        ('campaigns', '0003_category_products'),
    ]

    operations = [
        migrations.RenameModel('BasketDiscountAmount', 'CartDiscountAmount'),
        migrations.RenameModel('BasketDiscountPercentage', 'CartDiscountPercentage'),
        migrations.RenameModel('BasketDiscountEffect', 'CartDiscountEffect'),
        migrations.RenameModel('BasketCondition', 'CartCondition'),
        migrations.RenameModel('BasketLineEffect', 'CartLineEffect'),
    ]
