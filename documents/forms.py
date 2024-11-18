from django import forms
from datetime import datetime
from .models import Outgoing, Incoming, Internal, Decree



class add_outgoing_form(forms.ModelForm):
    class Meta:
        model = Outgoing
        fields = ['id', 'reg_number', 'out_date', 'dept_from', 'dept_to', 'title', 'keywords', 'pdf_file']
        widgets = {
            'out_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',  # Optional placeholder
                'type': 'date',  # Use the native HTML5 date picker
            }),
        }

class add_incoming_form(forms.ModelForm):
    class Meta:
        model = Incoming
        fields = ['id', 'orig_number', 'reg_number', 'orig_date', 'reg_date', 'dept_from', 'dept_to', 'title', 'keywords', 'pdf_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            if kwargs['instance'].orig_date:
                self.initial['orig_date'] = kwargs['instance'].orig_date.strftime('%Y-%m-%d')
            if kwargs['instance'].reg_date:
                self.initial['reg_date'] = kwargs['instance'].reg_date.strftime('%Y-%m-%d')


class add_internal_form(forms.ModelForm):
    class Meta:
        model = Internal
        fields = ['id', 'reg_number', 'int_date', 'dept_from', 'dept_to', 'title', 'keywords', 'pdf_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            if kwargs['instance'].int_date:
                self.initial['int_date'] = kwargs['instance'].int_date.strftime('%Y-%m-%d')


class add_decree_form(forms.ModelForm):
    class Meta:
        model = Decree
        fields = ['id', 'dec_date', 'dec_number', 'title', 'keywords', 'pdf_file', 'attach']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.initial['dec_date'] = kwargs['instance'].dec_date.strftime('%Y-%m-%d')
