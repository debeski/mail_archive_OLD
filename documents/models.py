from django.db import models
import uuid
from django.core.validators import RegexValidator

# Define the regex validator at the module level:
number_validator = RegexValidator(
    regex=r'^[0-9/-]*$',  # Only allows digits, dashes, and slashes
    message='Enter a valid number with dashes or slashes.',
    code='invalid_number'
)

# PDF & Attachment Naming Functions:
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
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Affiliate(models.Model):
    """Model representing an affiliate."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Minister(models.Model):
    """Model representing a minister."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Government(models.Model):
    """Model representing a government entity."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# The 4 Primary Mail Models:
class Incoming(models.Model):
    """Model representing incoming mail."""
    number = models.CharField(
        max_length=10,
        validators=[number_validator],  # Reuse the validator
        blank=False,
        null=False
    )
    orig_number = models.CharField(max_length=10, blank=True)
    date = models.DateField(blank=False)
    orig_date = models.DateField(blank=True)
    dept_from = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='incoming_affiliates')
    dept_to = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='incoming_departments')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.CharField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Outgoing(models.Model):
    """Model representing outgoing mail."""
    number = models.CharField(
        max_length=10,
        validators=[number_validator],
        blank=False,
        null=False
    )
    date = models.DateField(blank=False)
    dept_from = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='outgoing_departments')
    dept_to = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='outgoing_affiliates')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.CharField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Internal(models.Model):
    """Model representing internal mail between departments."""
    number = models.CharField(
        max_length=10,
        validators=[number_validator],
        blank=True,
        null=True
    )
    date = models.DateField(blank=True)
    dept_from = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='internal_departments_from')
    dept_to = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='internal_departments_to')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.CharField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Decree(models.Model):
    """Model representing a monister decree."""
    number = models.CharField(
        max_length=10,
        validators=[number_validator],
        blank=True,
        null=True
    )
    date = models.DateField(blank=False)
    minister = models.ForeignKey(Minister, on_delete=models.CASCADE, related_name='decrees')
    government = models.ForeignKey(Government, on_delete=models.CASCADE, related_name='decrees')
    title = models.CharField(max_length=255, blank=False)
    keywords = models.CharField(max_length=999, blank=True)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    attach = models.FileField(upload_to=get_attach_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    