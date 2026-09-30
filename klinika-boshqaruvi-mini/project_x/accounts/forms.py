from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Telefon raqam'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'avatar', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Foydalanuvchi nomi'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Parol'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Parolni tasdiqlang'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Foydalanuvchi nomi'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Parol'})


class UpdateProfileForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Telefon raqam'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Foydalanuvchi nomi'})