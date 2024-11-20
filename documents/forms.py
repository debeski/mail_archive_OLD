from django import forms
from .models import Outgoing, Incoming, Internal, Decree, Department, Affiliate, Minister, Government



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class AffiliateForm(forms.ModelForm):
    class Meta:
        model = Affiliate
        fields = ['name']

class MinisterForm(forms.ModelForm):
    class Meta:
        model = Minister
        fields = ['name']

class GovernmentForm(forms.ModelForm):
    class Meta:
        model = Government
        fields = ['name']



class AddOutgoingForm(forms.ModelForm):
    """Form for creating or updating outgoing mail."""
    
    class Meta:
        model = Outgoing
        fields = ['number', 'date', 'dept_from', 'dept_to', 'title', 'keywords', 'pdf_file']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل رقم الرسالة',
                'required': 'required'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',  # Keep this if you want larger input
                'placeholder': 'YYYY-MM-DD',
                'type': 'date',
                'required': 'required'
            }),
            'dept_from': forms.Select(attrs={
                'class': 'form-select form-select-lg',  # Keep this for consistency
                'required': 'required'
            }),
            'dept_to': forms.Select(attrs={
                'class': 'form-select form-select-lg',  # Keep this for consistency
                'required': 'required'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل العنوان',
                'required': 'required'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الكلمات المفتاحية',
                'required': 'required'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }


class AddIncomingForm(forms.ModelForm):
    """Form for creating or updating incoming mail."""
    
    class Meta:
        model = Incoming
        fields = ['number', 'orig_number', 'date', 'orig_date', 'dept_from', 'dept_to', 'title', 'keywords', 'pdf_file']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل رقم الرسالة',
                'required': 'required'
            }),
            'orig_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل الرقم الأصلي',
                'required': 'required'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date',
                'required': 'required'
            }),
            'orig_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date',
                'required': 'required'
            }),
            'dept_from': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': 'required'
            }),
            'dept_to': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': 'required'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل العنوان',
                'required': 'required'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الكلمات المفتاحية',
                'required': 'required'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }


class AddInternalForm(forms.ModelForm):
    """Form for creating or updating internal mail."""
    
    class Meta:
        model = Internal
        fields = ['number', 'date', 'dept_from', 'dept_to', 'title', 'keywords', 'pdf_file']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل رقم الرسالة',
                'required': 'required'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date',
                'required': 'required'
            }),
            'dept_from': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': 'required'
            }),
            'dept_to': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': 'required'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل العنوان',
                'required': 'required'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الكلمات المفتاحية',
                'required': 'required'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }


class AddDecreeForm(forms.ModelForm):
    """Form for creating or updating a decree."""
    
    class Meta:
        model = Decree
        fields = ['number', 'date', 'minister', 'government', 'title', 'keywords', 'pdf_file', 'attach']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل رقم القرار',
                'required': 'required'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date',
                'required': 'required'
            }),
            'minister': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': 'required'
            }),
            'government': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': 'required'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ادخل العنوان',
                'required': 'required'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الكلمات المفتاحية',
                'required': 'required'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'attach': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }
