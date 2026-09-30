from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'model_number', 'category', 'description', 'price', 'condition', 'image', 'is_available']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_available':
                field.widget.attrs['class'] = 'form-checkbox'
            elif name == 'image':
                field.widget.attrs['class'] = 'form-file'
            else:
                field.widget.attrs['class'] = 'form-input'
