from django import forms
import re
from .models import Outgoing, Incoming, Internal, Decree, Department, Affiliate, Minister, Government, Report


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        labels = {
            'name': 'اسم الادارة او المكتب',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }
        

class AffiliateForm(forms.ModelForm):
    class Meta:
        model = Affiliate
        fields = ['name']
        labels = {
            'name': 'اسم الجهة',
            "is_attached": "هل جهة تابعة للوزارة؟"
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'is_attached': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class GovernmentForm(forms.ModelForm):
    class Meta:
        model = Government
        fields = ['name']
        labels = {
            'name': 'اسم الحكومة',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }


class MinisterForm(forms.ModelForm):
    government = forms.ModelMultipleChoiceField(
        queryset=Government.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-inline'}),  # Add a custom class here
        required=True,
        label='الحكومات'
    )

    class Meta:
        model = Minister
        fields = ['name', 'government']  # Use 'governments' instead of 'government'
        labels = {
            'name': 'اسم الوزير',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }


class AddOutgoingForm(forms.ModelForm):
    """Form for creating or updating outgoing mail."""

    class Meta:
        model = Outgoing
        fields = ['number', 'date', 'deptartment', 'affiliate', 'title', 'keywords', 'pdf_file']
        labels = {
            'number': 'رقم الرسالة:',
            'date': 'تاريخ الرسالة: (يوم-شهر-سنة)',
            'dept_from': 'من (إدارة):',
            'dept_to': 'إلى (جهة):',
            'title': 'العنوان:',
            'keywords': 'الكلمات المفتاحية:',
            'pdf_file': 'ملف PDF',
        }
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',  # Larger input field
                'placeholder': 'YYYY-MM-DD',  # Placeholder for the user
                'type': 'text',  # Set as text input for Flatpickr
                'required': 'required',
                'autocomplete': 'off'
            }),
            'deptartment': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
            }),
            'affiliate': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '',
                'style': 'height: 150px;'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg'
            }),
        }


class AddIncomingForm(forms.ModelForm):
    """Form for creating or updating incoming mail."""
    
    class Meta:
        model = Incoming
        fields = ['number', 'orig_number', 'date', 'orig_date', 'affiliate', 'deptartment', 'title', 'keywords', 'pdf_file']
        labels = {
            'number': 'رقم التسجيل:',
            'orig_number': 'رقم الرسالة الإشاري:',
            'date': 'تاريخ التسجيل: (يوم-شهر-سنة)',
            'orig_date': 'تاريخ الرسالة: (يوم-شهر-سنة)',
            'dept_from': 'من (جهة):',
            'dept_to': 'إلى (إدارة):',
            'title': 'العنوان:',
            'keywords': 'الكلمات المفتاحية:',
            'pdf_file': 'ملف PDF',
        }
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'orig_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-md dateclass',
                'placeholder': '',
                'type': 'date',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'orig_date': forms.DateInput(attrs={
                'class': 'form-control form-control-md dateclass',
                'placeholder': '',
                'type': 'date',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'affiliate': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
            }),
            'deptartment': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '',
                'style': 'height: 150px;'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg'
            }),
        }


class AddInternalForm(forms.ModelForm):
    """Form for creating or updating internal mail."""
    
    class Meta:
        model = Internal
        fields = ['number', 'date', 'deptartment', 'deptartment_to', 'title', 'keywords', 'pdf_file']
        labels = {
            'number': 'رقم الرسالة:',
            'date': 'تاريخ الرسالة: (يوم-شهر-سنة)',
            'dept_from': 'من:',
            'dept_to': 'إلى:',
            'title': 'العنوان:',
            'keywords': 'الكلمات المفتاحية:',
            'pdf_file': 'ملف PDF',
        }
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '',
                'type': 'date',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'deptartment': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'deptartment_to': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '',
                'style': 'height: 150px;'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg'
            }),
        }


class AddDecreeForm(forms.ModelForm):
    """Form for creating or updating a decree."""
    
    class Meta:
        model = Decree
        fields = ['number', 'date', 'minister', 'government', 'title', 'keywords', 'pdf_file', 'attach']
        labels = {
            'number': 'رقم القرار:',
            'date': 'تاريخ القرار: (يوم-شهر-سنة)',
            'minister': 'الوزير:',
            'government': 'الحكومة:',
            'title': 'العنوان:',
            'keywords': 'الكلمات المفتاحية:',
            'pdf_file': 'ملف PDF',
            'attach': 'ملف مرفق',
        }
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '',
                'type': 'date',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'minister': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'government': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '',
                'style': 'height: 150px;'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'attach': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class AddReportForm(forms.ModelForm):
    """Form for creating or updating a decree."""
    
    class Meta:
        model = Report
        fields = ['number', 'date', 'title', 'keywords', 'pdf_file']
        labels = {
            'number': 'رقم الوثيقة:',
            'date': 'تاريخ الوثيقة: (يوم-شهر-سنة)',
            'title': 'العنوان:',
            'keywords': 'الكلمات المفتاحية:',
            'pdf_file': 'ملف PDF',
        }
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '',
                'type': 'date',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': 'required'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '',
                'style': 'height: 150px;'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

