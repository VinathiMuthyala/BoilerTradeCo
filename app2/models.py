from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class QualityTag(models.Model):
  tag = models.CharField(max_length=100, choices = [
       ('Like New', 'Like New'),
       ('Good', 'Good'),
       ('Acceptable', 'Acceptable'),
   ])

   # get_quality()
  def __str__(self):
       return self.tag
  
   # will connect this in front end later
  def set_quality(self, quality):
       self.tag = quality


class CategoryTag(models.Model):
   tag= models.CharField(max_length=100, choices = [
       ('Furniture', 'Furniture'),
       ('Appliances', 'Appliances'),
       ('Textbooks', 'Textbooks'),
       ('School supplies', 'School supplies'),
       ('Clothing', 'Clothing'),
       ('Game tickets', 'Game tickets'),
   ])
   # get_category()
   def __str__(self):
       return self.tag

class ProductInfo(models.Model):
   seller_email = models.CharField(max_length=100, primary_key=True, unique=True)
   name = models.CharField(max_length=100)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   description = models.TextField()
   quality_tag = models.ForeignKey(QualityTag, on_delete=models.SET_NULL, null=True, blank=True)
   category_tag = models.ForeignKey(CategoryTag, on_delete=models.SET_NULL, null=True, blank=True)
   date_posted = models.TextField(default=0000-00-00)
   #seller_name = models.CharField(max_length=100)
   #seller_phone_number = models.IntegerField(validators=[MaxValueValidator(9999999999)])
   #seller_instagram = models.CharField(max_length=30) # max length of valid instagram username
   #is_favorited = models.BooleanField(default=False)

   @classmethod
   def create_product(cls, seller_email, name=None, price=None, description=None, quality_tag=None, category_tag=None, date_posted=None):
       existing_product = cls.objects.filter(seller_email=seller_email).first()

       if existing_product:
                # Update the existing product
                existing_product.name = name
                existing_product.price = price
                existing_product.description = description
                existing_product.quality_tag, _ = QualityTag.objects.get_or_create(tag=quality_tag)
                existing_product.category_tag, _ = CategoryTag.objects.get_or_create(tag=category_tag)
                existing_product.date_posted = date_posted
                existing_product.save()
                return existing_product
       else:
                # Create a new product
                quality_tag_instance, _ = QualityTag.objects.get_or_create(tag=quality_tag)
                category_tag_instance, _ = CategoryTag.objects.get_or_create(tag=category_tag)

                return cls.objects.create(
                    seller_email=seller_email,
                    name=name,
                    price=price,
                    description=description,
                    quality_tag=quality_tag_instance,
                    category_tag=category_tag_instance,
                    date_posted=date_posted
        )



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
  
   def set_name(self, name):
       self.name = name
  
   def get_price(self):
       return self.price
  
   def set_price(self, price):
       self.price = price

   def get_description(self):
       return self.description
  
   def set_description(self, description):
       self.description = description
  
#    def get_seller_name(self):
#        return self.seller_name
  
#    def set_seller_name(self, seller_name):
#        self.seller_name = seller_name
  
   def get_seller_email(self):
       return self.seller_email
  
   def set_seller_email(self, seller_email):
       self.seller_email = seller_email
  
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
        return f"Listing for Product: {self.product.name} - Seller: {self.product.seller_email}"
        # return str(self.product)