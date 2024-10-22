from django import forms
from .models import Decree  # Replace with your actual model

class add_decree_form(forms.ModelForm):
    class Meta:
        model = Decree
        fields = ['dec_date', 'dec_number', 'title', 'keywords', 'pdf_file', 'attach']