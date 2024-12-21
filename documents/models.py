from django.db import models
import uuid
from django.core.validators import RegexValidator
import re

# Define REGex Validator at moduler level:
number_validator = RegexValidator(
    regex=r'^[0-9/-]*$',  # Only allows digits, dashes, and slashes
    message='Enter a valid number with dashes or slashes.',
    code='invalid_number'
)

# PDF Files Naming Functions:
def generate_random_filename(instance, filename):
    """Generate a random filename for uploaded files."""
    random_filename = f"{uuid.uuid4().hex}.pdf"
    model_name = instance.__class__.__name__.lower()
    return f'{model_name}/{random_filename}'

def get_pdf_upload_path(instance, filename):
    """Get the upload path for PDF files."""
    return f'pdfs/{generate_random_filename(instance, filename)}'

def get_attach_upload_path(instance, filename):
    """Get the upload path for attachment files."""
    return f'attach/{generate_random_filename(instance, filename)}'


# Section Models:
class Department(models.Model):
    """Model representing a department."""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "الادارة او المكتب"
        verbose_name_plural = "الادارات و المكاتب"
        ordering = ['-created_at']  # Sort by created_at in descending order

    def __str__(self):
        return self.name

class Affiliate(models.Model):
    """Model representing an affiliate."""
    name = models.CharField(max_length=255, unique=True)
    is_attached = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "الجهة"
        verbose_name_plural = "الجهات"
        ordering = ['-created_at']  # Sort by created_at in descending order

    def __str__(self):
        return self.name

class Government(models.Model):
    """Model representing a government entity."""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "الحكومة"
        verbose_name_plural = "الحكومات"
        ordering = ['-created_at']  # Sort by created_at in descending order

    def __str__(self):
        return self.name

class Minister(models.Model):
    """Model representing a minister."""
    name = models.CharField(max_length=255, unique=True)
    government = models.ManyToManyField(Government, related_name='minister_on_duty')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "الوزير"
        verbose_name_plural = "الوزراء"
        ordering = ['-created_at']  # Sort by created_at in descending order

    def __str__(self):
        return self.name


# Primary Mail Models:
class Incoming(models.Model):
    """Model representing incoming mail."""
    number = models.CharField(
        max_length=10,
        validators=[number_validator],  # Reuse the validator
        blank=False,
        null=False
    )
    orig_number = models.CharField(
        max_length=10,
        validators=[number_validator],  # Reuse the validator
        blank=False,
        null=False
    )
    date = models.DateField(blank=False)
    orig_date = models.DateField(blank=True)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.PROTECT, related_name='incoming_affiliates')
    deptartment = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='incoming_departments')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.TextField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "بريد وارد"
        verbose_name_plural = "البريد الوارد"

    def __str__(self):
        return self.title
    
    def get_last_segment(self):
        segments = re.split(r'[\\\-\.]', self.number)
        return int(segments[-1]) if segments[-1].isdigit() else 0  # Fall

class Outgoing(models.Model):
    """Model representing outgoing mail."""
    number = models.CharField(
        max_length=10,
        validators=[number_validator],
        blank=False,
        null=False
    )
    date = models.DateField(blank=False)
    deptartment = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='outgoing_departments')
    affiliate = models.ForeignKey(Affiliate, on_delete=models.PROTECT, related_name='outgoing_affiliates')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.TextField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "بريد صادر"
        verbose_name_plural = "البريد الصادر"

    def __str__(self):
        return self.title
    
    def get_last_segment(self):
        segments = re.split(r'[\\\-\.]', self.number)
        return int(segments[-1]) if segments[-1].isdigit() else 0  # Fall

class Internal(models.Model):
    """Model representing internal mail between departments."""
    number = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(blank=True)
    deptartment = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='internal_departments_from')
    deptartment_to = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='internal_departments_to')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.TextField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "مذكرة داخلية"
        verbose_name_plural = "المذكرات الداخلية"
    
    def get_last_segment(self):
        segments = re.split(r'[\\\-\.]', self.number)
        return int(segments[-1]) if segments[-1].isdigit() else 0  # Fall
    
    def __str__(self):
        return self.title

    @property
    def get_model_name(self):
        return "مذكرات داخلية"

class Decree(models.Model):
    """Model representing a minister decree."""
    number = models.CharField(max_length=10, blank=False, null=False)
    date = models.DateField(blank=False)
    minister = models.ForeignKey(Minister, on_delete=models.PROTECT, related_name='decrees')
    government = models.ForeignKey(Government, on_delete=models.PROTECT, related_name='decrees')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.TextField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    attach = models.FileField(upload_to=get_attach_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "قرار"
        verbose_name_plural = "القرارات"

    def __str__(self):
        return self.title
    
    def get_last_segment(self):
        segments = re.split(r'[\\\-\.]', self.number)
        return int(segments[-1]) if segments[-1].isdigit() else 0  # Fall

class Report(models.Model):
    """Ambiguous Model representing a report of some sort."""
    number = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True)
    title = models.CharField(max_length=255, blank=False)
    keywords = models.TextField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "تقرير"
        verbose_name_plural = "التقارير"

    def __str__(self):
        return self.title
    
    def get_last_segment(self):
        segments = re.split(r'[\\\-\.]', self.number)
        return int(segments[-1]) if segments[-1].isdigit() else 0  # Fall

