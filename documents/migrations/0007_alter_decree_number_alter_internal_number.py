# Generated by Django 5.1.3 on 2024-11-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_alter_affiliate_name_alter_department_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decree',
            name='number',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='internal',
            name='number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
