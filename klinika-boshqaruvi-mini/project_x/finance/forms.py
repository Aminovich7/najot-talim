from django import forms
from .models import Doctor, Consultation, Surgery, Room


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialty']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism',
                'maxlength': '50'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiya',
                'maxlength': '50'
            }),
            'specialty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mutaxassislik',
                'maxlength': '50'
            }),
        }
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'specialty': 'Mutaxassislik',
        }


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['type', 'receipt_number', 'date', 'doctor_percent', 'minus_beshming', 'amount', 'doctor']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'doctor_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': 'Shifokor foizi'
            }),
            'minus_beshming': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minus beshming'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Summa'
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'type': 'Turi',
            'receipt_number': 'Chek Raqami',
            'date': 'Sana',
            'doctor_percent': 'Shifokor foizi (%)',
            'minus_beshming': 'Minus beshming',
            'amount': 'Summa',
            'doctor': 'Shifokor',
        }


class SurgeryForm(forms.ModelForm):
    class Meta:
        model = Surgery
        fields = ['receipt_number', 'amount', 'surgery_expense', 'doctor_percent', 'doctor', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Summa'
            }),
            'surgery_expense': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Operatsiya xarajati'
            }),
            'doctor_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': 'Shifokor foizi'
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'receipt_number': 'Chek Raqami',
            'amount': 'Summa',
            'surgery_expense': 'Operatsiya xarajati',
            'doctor_percent': 'Shifokor foizi (%)',
            'doctor': 'Shifokor',
            'date': 'Sana',
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['receipt_number', 'amount', 'doctor_percent', 'doctor', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Summa'
            }),
            'doctor_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': 'Shifokor foizi'
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'receipt_number': 'Chek Raqami',
            'amount': 'Summa',
            'doctor_percent': 'Shifokor foizi (%)',
            'doctor': 'Shifokor',
            'date': 'Sana',
        }