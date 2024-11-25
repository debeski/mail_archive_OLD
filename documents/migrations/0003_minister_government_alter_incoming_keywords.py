# Generated by Django 5.1.3 on 2024-11-22 01:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_decree_government_alter_decree_minister_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='minister',
            name='government',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='minister_on_duty', to='documents.government'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incoming',
            name='keywords',
            field=models.TextField(blank=True, max_length=999),
        ),
    ]
