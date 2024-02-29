from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# contains 2 values
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Profile(models.Model):
    # will delete the profile when the user is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' # show how we want it to be displayed