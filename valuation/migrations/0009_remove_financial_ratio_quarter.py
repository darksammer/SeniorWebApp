# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 06:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0008_auto_20170420_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financial_ratio',
            name='quarter',
        ),
    ]