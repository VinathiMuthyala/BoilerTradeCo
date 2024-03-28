from django.contrib import admin
from django.contrib.admin.exceptions import AlreadyRegistered

from .models import ProductInfo, CategoryTag, QualityTag # add ProductListing back

# Register your models here.

models = [ProductInfo, CategoryTag, QualityTag] # add ProductListing back

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass