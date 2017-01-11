# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='general_information',
            old_name='dividend_payout_per_year',
            new_name='dividend_payout_amount_per_year',
        ),
        migrations.AlterField(
            model_name='general_information',
            name='fund_type',
            field=models.CharField(choices=[('LF', 'Leasehold & Freehold'), ('L', 'Leasehold'), ('F', 'Freehold')], default='L', max_length=20),
        ),
    ]
