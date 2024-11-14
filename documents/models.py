from django.db import models
import os
import datetime


# Create your models here.

def get_file_date(instance):
    if isinstance(instance, Outgoing):
        return instance.out_date
    elif isinstance(instance, Incoming):
        return instance.reg_date  # Adjust as needed for other models
    elif isinstance(instance, Internal):
        return instance.int_date
    elif isinstance(instance, Decree):
        return instance.dec_date
    return None

def get_pdf_upload_path(instance, filename):
    date_part = get_file_date(instance)
    date_part = date_part.strftime('%Y-%m-%d') if date_part else 'unknown_date'
    model_name = instance.__class__.__name__.lower()
    
    # Generate the filename using the specified format
    return f'pdfs/{model_name}/{instance.reg_number}_{date_part}.pdf'

def get_attach_upload_path(instance, filename):
    date_part = get_file_date(instance)
    date_part = date_part.strftime('%Y-%m-%d') if date_part else 'unknown_date'
    model_name = instance.__class__.__name__.lower()
    
    # Generate the filename using the specified format
    return f'attach/{model_name}/{instance.reg_number}_{date_part}.pdf'


class Incoming(models.Model):
    id = models.AutoField(primary_key=True)
    orig_date = models.DateField(blank=False, null=False)
    reg_date = models.DateField(blank=False, null=False)
    orig_number = models.CharField(max_length=100, blank=True, null=True)
    reg_number = models.CharField(max_length=100, blank=False, null=False)
    dept_from = models.CharField(max_length=100, blank=False, null=False)
    dept_to = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/incoming/', blank=True)
    attach = models.FileField(upload_to='attach/incoming', blank=True)

    def __str__(self):
        return self.title

class Outgoing(models.Model):
    id = models.AutoField(primary_key=True)
    out_date = models.DateField(blank=False, null=False)
    reg_number = models.CharField(max_length=100, blank=False, null=False)
    dept_from = models.CharField(max_length=100, blank=False, null=False)
    dept_to = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    attach = models.FileField(upload_to=get_attach_upload_path, blank=True)

    def __str__(self):
        return self.title

class Internal(models.Model):
    id = models.AutoField(primary_key=True)
    int_date = models.DateField(blank=True, null=True)
    reg_number = models.CharField(max_length=100, blank=True, null=True)
    dept_from = models.CharField(max_length=100, blank=False, null=False)
    dept_to = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/internal/', blank=True)
    attach = models.FileField(upload_to='attach/internal/', blank=True)

class Decree(models.Model):
    id = models.AutoField(primary_key=True)
    dec_date = models.DateField(blank=False, null=False)
    dec_number = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/decree/', blank=True)
    attach = models.FileField(upload_to='attach/decree/', blank=True)