# Generated by Django 5.1.2 on 2024-10-21 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Decree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dec_date', models.DateField()),
                ('dec_number', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('pdf_file', models.FileField(upload_to='pdfs/decree/')),
                ('attach', models.FileField(blank=True, upload_to='attach/decree/')),
            ],
        ),
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orig_date', models.DateField()),
                ('reg_date', models.DateField()),
                ('orig_number', models.CharField(blank=True, max_length=100, null=True)),
                ('reg_number', models.CharField(max_length=100)),
                ('dept_from', models.CharField(max_length=100)),
                ('dept_to', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('pdf_file', models.FileField(upload_to='pdfs/incoming/')),
                ('attach', models.FileField(blank=True, upload_to='attach/incoming')),
            ],
        ),
        migrations.CreateModel(
            name='Internal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_date', models.DateField(blank=True, null=True)),
                ('reg_number', models.CharField(blank=True, max_length=100, null=True)),
                ('dept_from', models.CharField(max_length=100)),
                ('dept_to', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('pdf_file', models.FileField(upload_to='pdfs/internal/')),
                ('attach', models.FileField(blank=True, upload_to='attach/internal/')),
            ],
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_date', models.DateField()),
                ('reg_number', models.CharField(max_length=100)),
                ('dept_from', models.CharField(max_length=100)),
                ('dept_to', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('pdf_file', models.FileField(upload_to='pdfs/outgoing/')),
                ('attach', models.FileField(blank=True, upload_to='attach/outgoing/')),
            ],
        ),
    ]
