# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-22 13:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0005_auto_20170222_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financial_statement',
            name='quarter',
        ),
    ]
