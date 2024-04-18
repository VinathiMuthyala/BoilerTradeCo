from django import forms
from django.utils import timezone

from .models import ProductInfo, QualityTag, CategoryTag

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewProductForm, self).__init__(*args, **kwargs)
        self.fields['date_posted'].initial = timezone.localtime(timezone.now()).date().strftime('%Y-%m-%d')
        self.fields['date_posted'].widget.attrs['readonly'] = True

    class Meta:
        model = ProductInfo
        fields = ('seller_email', 'name', 'price', 'description', 'quality_tag', 'category_tag', 'is_sold', 'date_posted', 'image',)

class EditProductForm(forms.ModelForm):
    # previous_price = forms.DecimalField(required=False, widget=forms.HiddenInput)

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
                'class': 'input-classes',
                'onclick': 'showSoldMessage(this.checked);' 
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }