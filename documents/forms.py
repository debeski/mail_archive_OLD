from django import forms
from .models import Outgoing

class add_outgoing_form(forms.ModelForm):
    class Meta:
        model = Outgoing
        fields = ['id', 'reg_number', 'out_date', 'dept_from', 'dept_to', 'title', 'keywords', 'pdf_file', 'attach']