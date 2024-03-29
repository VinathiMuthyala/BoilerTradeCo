from django import forms

from .models import ProductInfo

class NewProductForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ('seller_email', 'name', 'price', 'description', 'quality_tag', 'category_tag', 'is_sold', 'date_posted', 'image',)