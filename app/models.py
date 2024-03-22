from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# contains 2 values
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Profile(models.Model):
    # will delete the profile when the user is deleted
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_images/')
    
    def __str__(self):
        return str(self.user)