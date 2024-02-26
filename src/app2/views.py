from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def layout(request):
    return render(request, 'authentication/light-dark-toggle.html') # confirm if this is okay productdir/index.html before

def add_product(request):
    return render(request, 'productdir/add-product.html')

# Backend code

class Product():
    def __init__(self, name, price, description, quality_tag, category_tag, seller_name, seller_email, seller_phone, seller_instagram, is_favorited = False):
        self.name = name
        self.price = price
        self.description = description
        self.quality_tag = QualityTag()
        self.category_tag = CategoryTag()
        self.seller_name = seller_name
        self.seller_email = seller_email
        self.seller_phone = seller_phone
        self.seller_instagram = seller_instagram
        self.is_favorited = is_favorited
    def get_name(self):
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
    def get_seller_name(self):
        return self.seller_name
    def set_seller_name(self, seller_name):
        self.seller_name = seller_name
    def get_seller_email(self):
        return self.seller_email
    def set_seller_email(self, seller_email):
        self.seller_email = seller_email
    def get_seller_phone(self):
        return self.seller_phone
    def set_seller_phone(self, seller_phone):
        self.seller_phone = seller_phone
    def get_seller_instagram(self):
        return self.seller_instagram
    def set_seller_instagram(self, seller_instagram):
        self.seller_instagram = seller_instagram
    def get_is_favorited(self):
        return self.is_favorited
    def set_is_favorited(self, is_favorited):
        self.is_favorited = is_favorited
    
class QualityTag(Product):
    productQuality = [
        ('Like New'),
        ('Good'),
        ('Acceptable'),
    ]
    def get_quality(Product):
        return Product.quality_tag
    
    # will connect this in front end later
    def set_quality(self, quality):
        self.quality_tag = quality
    
class CategoryTag(Product):
    productCategory = [
        ('Furniture'),
        ('Appliances'),
        ('Textbooks'),
        ('School supplies'),
        ('Clothing'),
        ('Game tickets'),
    ]
    def get_category(Product):
        return Product.category
    
    def set_category(self, category):
        self.category = category

class ProductDirectory(Product):
    products = [

    ]

    def get_product(products, Product):
        for i in products:
            if products[i].name == Product.get_name():
                return products[i]
            
    def set_product(products, Product):
        products[len(products)] = Product