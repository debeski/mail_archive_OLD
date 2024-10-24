from django.db import models
from django.utils.text import slugify
import os
import datetime



# Create your models here.

def get_pdf_upload_path(instance, filename):
    """
    Generates a unique upload path for PDF files, using only the registration number and date.

    Args:
        instance (models.Model): The model instance for which the file is uploaded.
        filename (str): The original filename provided by the user (ignored).

    Returns:
        str: The complete upload path for the PDF file.
    """

    # Extract the date from the filename (if present)
    filename_without_extension = os.path.splitext(filename)[0]
    try:
        date_part = datetime.datetime.strptime(filename_without_extension, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        # If the filename doesn't match the date format, use the current date
        date_part = datetime.date.today().strftime('%Y-%m-%d')

    # Combine registration number and date
    return f'pdfs/outgoing/{instance.reg_number}_{date_part}.pdf'


def get_attach_upload_path(instance, filename):
    """
    Generates a unique upload path for attachment files, using only the registration number and date.

    Args:
        instance (models.Model): The model instance for which the file is uploaded.
        filename (str): The original filename provided by the user (ignored).

    Returns:
        str: The complete upload path for the attachment file.
    """

    # Extract the date from the filename (if present)
    filename_without_extension = os.path.splitext(filename)[0]
    try:
        date_part = datetime.datetime.strptime(filename_without_extension, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        # If the filename doesn't match the date format, use the current date
        date_part = datetime.date.today().strftime('%Y-%m-%d')

    # Combine registration number and date
    return f'attach/outgoing/{instance.reg_number}_{date_part}.attach'


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