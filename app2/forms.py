from django import forms

from .models import ProductInfo

class NewProductForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ('product_id', 'seller_email', 'name', 'price', 'description', 'quality_tag', 'category_tag', 'date_posted',)