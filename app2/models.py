from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class QualityTag(models.Model):
    LIKE_NEW = 'Like New'
    GOOD = 'Good'
    ACCEPTABLE = 'Acceptable'
    TAG_CHOICES = [
        (LIKE_NEW, 'Like New'),
        (GOOD, 'Good'),
        (ACCEPTABLE, 'Acceptable'),
    ]
    tag = models.CharField(max_length=100, choices=TAG_CHOICES)
    # get_quality()
    def __str__(self):
        return self.tag
    # will connect this in front end later
    # def set_quality(self, quality):
    #    self.tag = quality
    class Meta:
       verbose_name_plural = 'QualityTag'


class CategoryTag(models.Model):
    FURNITURE = 'Furniture'
    APPLIANCES = 'Appliances'
    TEXTBOOKS = 'Textbooks'
    SCHOOL_SUPPLIES = 'School Supplies'
    CLOTHING = 'Clothing'
    GAME_TICKETS = 'Game Tickets'
    OTHER = 'Other'
    TAG_CHOICES = [
        (FURNITURE, 'Furniture'),
        (APPLIANCES, 'Appliances'),
        (TEXTBOOKS, 'Textbooks'),
        (SCHOOL_SUPPLIES, 'School Supplies'),
        (CLOTHING, 'Clothing'),
        (GAME_TICKETS, 'Game Tickets'),
        (OTHER, 'Other'),
    ]
    tag = models.CharField(max_length=100, choices=TAG_CHOICES)
    print(tag)
   # get_category()
    def __str__(self):
       return self.tag
    class Meta:
       ordering = ('tag',)
       verbose_name_plural = 'CategoryTag'

class ProductInfo(models.Model):
   # product_key = models.AutoField(primary_key=True, default='DEFAULT', unique=True, db_index=True)
   # product_id = models.IntegerField(primary_key=True, default=0, unique=True)
   product_id = models.AutoField(primary_key=True)
   seller_email = models.ForeignKey(User, null=False, related_name='products', on_delete=models.CASCADE)
   name = models.CharField(max_length=100)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   previous_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   description = models.TextField(blank=True, null=True)
   quality_tag = models.ForeignKey(QualityTag, null=False, related_name='products', on_delete=models.CASCADE)
   category_tag = models.ForeignKey(CategoryTag, null=False, related_name='products', on_delete=models.CASCADE)
   is_sold = models.BooleanField(default=False)
   date_posted = models.DateField() #default=0000-00-00
   image = models.ImageField(upload_to='product_images', blank=True, null=True)
   price_changed = models.BooleanField(default=False)
   #seller_name = models.CharField(max_length=100)
   #seller_phone_number = models.IntegerField(validators=[MaxValueValidator(9999999999)])
   #seller_instagram = models.CharField(max_length=30) # max length of valid instagram username
   #is_favorited = models.BooleanField(default=False)

#    @classmethod
#    def create_product(cls, seller_email, name=None, price=None, description=None, quality_tag=None, category_tag=None, date_posted=None):
#        existing_product = cls.objects.filter(seller_email=seller_email).first()

#        if existing_product:
#                 # Update the existing product
#                 existing_product.name = name
#                 existing_product.price = price
#                 existing_product.description = description
#                 existing_product.quality_tag, _ = QualityTag.objects.get_or_create(tag=quality_tag)
#                 existing_product.category_tag, _ = CategoryTag.objects.get_or_create(tag=category_tag)
#                 existing_product.date_posted = date_posted
#                 existing_product.save()
#                 return existing_product
#        else:
#                 # Create a new product
#                 quality_tag_instance, _ = QualityTag.objects.get_or_create(tag=quality_tag)
#                 category_tag_instance, _ = CategoryTag.objects.get_or_create(tag=category_tag)

#                 return cls.objects.create(
#                     seller_email=seller_email,
#                     name=name,
#                     price=price,
#                     description=description,
#                     quality_tag=quality_tag_instance,
#                     category_tag=category_tag_instance,
#                     date_posted=date_posted
#         )



    #    return ProductInfo.create_product(name, price, seller_email, description, quality_tag, category_tag, date_posted)
    #    quality_tag_instance, _ = QualityTag.objects.get_or_create(tag=quality_tag)
    #    category_tag_instance, _ = CategoryTag.objects.get_or_create(tag=category_tag)

    #    return cls.objects.create(
    #         seller_email=seller_email,
    #         name=name,
    #         price=price,
    #         description=description,
    #         quality_tag=quality_tag_instance,
    #         category_tag=category_tag_instance,
    #         date_posted=date_posted
    #     )
    # return self.__class__.objects.create(
    #         name=name,
    #         price=price,
    #         seller_email=seller_email,
    #         description=description,
    #         quality_tag=quality_tag,
    #         category_tag=category_tag,
    #         date_posted=date_posted
    # )

   # get_name()
   def __str__(self):
       return self.name
   class Meta:
       verbose_name_plural = 'ProductInfo'
  
#    def set_name(self, name):
#        self.name = name
  
#    def get_price(self):
#        return self.price
  
#    def set_price(self, price):
#        self.price = price

#    def get_description(self):
#        return self.description
  
#    def set_description(self, description):
#        self.description = description
  
#    def get_seller_name(self):
#        return self.seller_name
  
#    def set_seller_name(self, seller_name):
#        self.seller_name = seller_name
  
#    def get_seller_email(self):
#        return self.seller_email
  
#    def set_seller_email(self, seller_email):
#        self.seller_email = seller_email
  
#    def get_seller_phone_number(self):
#        return self.seller_phone_number
  
#    def set_seller_phone(self, seller_phone):
#        self.seller_phone = seller_phone
  
#    def get_seller_instagram(self):
#        return self.seller_instagram
  
#    def set_seller_instagram(self, seller_instagram):
#        self.seller_instagram = seller_instagram
  
#    def get_is_favorited(self):
#        return self.is_favorited
  
#    def set_is_favorited(self, is_favorited):
#        self.is_favorited = is_favorited

class ProductListing(models.Model):
    # will delete the listing when the product is deleted
    product = models.OneToOneField(ProductInfo, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Listing for Product: {self.product.name} - Seller: {self.product.seller_email}"
        # return str(self.product)
    
    class Meta:
       verbose_name_plural = 'ProductListing'

class Bookmark(models.Model):
    user = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    post = models.ForeignKey(ProductInfo, related_name='bookmarked_by', on_delete=models.CASCADE)

class Sales(models.Model):
    post = models.ForeignKey(ProductInfo, related_name='sold_by', on_delete=models.CASCADE)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)