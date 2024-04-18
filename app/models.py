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
    confirm = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    def __str__(self):
        return str(self.user)

class SellerRating(models.Model):
    seller_email = models.EmailField(default='example@example.com')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)