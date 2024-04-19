from django import forms

from django.contrib.auth.models import User
from .models import Profile

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = Profile
        fields = ['avatar']

class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 5}), required=False)
