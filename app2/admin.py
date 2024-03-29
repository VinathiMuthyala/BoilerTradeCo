from django.contrib import admin
from django.contrib.admin.exceptions import AlreadyRegistered

from .models import ProductListing, ProductInfo, CategoryTag, QualityTag

# Register your models here.

models = [ProductListing, ProductInfo, CategoryTag, QualityTag]

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass