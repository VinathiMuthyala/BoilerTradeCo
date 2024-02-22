from django.db import models

# Create your models here.

# contains 2 values
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()