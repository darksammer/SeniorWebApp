# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0007_auto_20170419_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dividend_yield',
            name='div_yield',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
