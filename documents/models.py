from django.db import models

# Create your models here.

from django.db import models

class Incoming(models.Model):
    orig_date = models.DateField(blank=False, null=False)
    reg_date = models.DateField(blank=False, null=False)
    orig_number = models.CharField(max_length=100, blank=True, null=True)
    reg_number = models.CharField(max_length=100, blank=False, null=False)
    dept_from = models.CharField(max_length=100, blank=False, null=False)
    dept_to = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/incoming/', blank=False)
    attach = models.FileField(upload_to='attach/incoming', blank=True)

class Outgoing(models.Model):
    out_date = models.DateField(blank=False, null=False)
    reg_number = models.CharField(max_length=100, blank=False, null=False)
    dept_from = models.CharField(max_length=100, blank=False, null=False)
    dept_to = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/outgoing/', blank=False)
    attach = models.FileField(upload_to='attach/outgoing/', blank=True)

    def __str__(self):
        return self.title

class Internal(models.Model):
    int_date = models.DateField(blank=True, null=True)
    reg_number = models.CharField(max_length=100, blank=True, null=True)
    dept_from = models.CharField(max_length=100, blank=False, null=False)
    dept_to = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/internal/', blank=False)
    attach = models.FileField(upload_to='attach/internal/', blank=True)

class Decree(models.Model):
    dec_date = models.DateField(blank=False, null=False)
    dec_number = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/decree/', blank=False)
    attach = models.FileField(upload_to='attach/decree/', blank=True)