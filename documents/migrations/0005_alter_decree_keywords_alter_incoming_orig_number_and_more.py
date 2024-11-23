# Generated by Django 5.1.3 on 2024-11-22 19:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_affiliate_is_attached'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decree',
            name='keywords',
            field=models.TextField(blank=True, max_length=999),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='orig_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='invalid_number', message='Enter a valid number with dashes or slashes.', regex='^[0-9/-]*$')]),
        ),
        migrations.AlterField(
            model_name='internal',
            name='keywords',
            field=models.TextField(blank=True, max_length=999),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='keywords',
            field=models.TextField(blank=True, max_length=999),
        ),
    ]
