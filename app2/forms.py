from django import forms

from .models import ProductInfo

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewProductForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ('seller_email', 'name', 'price', 'description', 'quality_tag', 'category_tag', 'is_sold', 'date_posted', 'image',)

class EditProductForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ('name', 'price', 'description', 'is_sold', 'image',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'is_sold': forms.CheckboxInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }