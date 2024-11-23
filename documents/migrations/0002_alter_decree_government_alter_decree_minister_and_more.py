# Generated by Django 5.1.3 on 2024-11-22 01:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decree',
            name='government',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='decrees', to='documents.government'),
        ),
        migrations.AlterField(
            model_name='decree',
            name='minister',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='decrees', to='documents.minister'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='dept_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_affiliates', to='documents.affiliate'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='dept_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_departments', to='documents.department'),
        ),
        migrations.AlterField(
            model_name='internal',
            name='dept_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='internal_departments_from', to='documents.department'),
        ),
        migrations.AlterField(
            model_name='internal',
            name='dept_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='internal_departments_to', to='documents.department'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='dept_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outgoing_departments', to='documents.department'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='dept_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outgoing_affiliates', to='documents.affiliate'),
        ),
    ]
