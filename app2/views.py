from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import models
from datetime import date
from django.contrib import messages
from .models import ProductInfo, ProductListing
from django.conf import settings
import os

# Create your views here.
def layout(request):
    return render(request, 'authentication/light-dark-toggle.html') # confirm if this is okay productdir/index.html before

def add_product(request):
    return render(request, 'productdir/add-product.html')

def add_listing(request):
    print("hello is this working")
    if request.method == "POST":
        if request.FILES.get('photo'):
            photo = request.FILES['photo']
            if photo.content_type.startswith('image'):
                if photo.size <= 800 * 1024:  # 800 KB in bytes
                    save_path = os.path.join(settings.MEDIA_ROOT, 'photos', photo.name)
                    with open(save_path, 'wb') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)
                else:
                    error_message = "File size exceeds the maximum allowed size (800KB). Please choose a smaller file."
                    messages.MessageFailure(error_message)
            else:
                error_message = "Invalid file type. Please upload an image (JPG, PNG, GIF)."
                messages.MessageFailure(error_message)
        else:
            error_message = "No file uploaded."
            messages.MessageFailure(error_message)
        if 'product_info' in request.POST:
            seller_email = request.POST.get('sellerEmail')
            product_name = request.POST.get('productName')
            product_price = request.POST.get('productPrice')
            product_description = request.POST.get('productDescription')
            quality_tag = request.POST.get('qualityTag')
            category_tag = request.POST.get('categoryTag')
            date_posted = date.today().strftime("%Y-%m-%d")
            img = photo
            print(product_name)
            print(product_price)
            print(seller_email)
            print(product_description)
            print(quality_tag)
            print(category_tag)
            print("the date: ", date_posted)

            myproduct = ProductInfo.create_product(
                seller_email=seller_email,
                name=product_name,
                price=product_price,
                description=product_description,
                quality_tag=quality_tag,
                category_tag=category_tag,
                date_posted=date_posted,
                photo=photo
            )
            # myproduct = ProductInfo.create_product(product_name, product_price, seller_email, product_description, quality_tag, category_tag, date_posted)
            #myproduct = ProductInfo(name=product_name, price=product_price, seller_email = seller_email, description=product_description, quality_tag=quality_tag, category_tag=category_tag, date_posted = date_posted)
            # myproduct.save()

            existing_product = get_object_or_404(ProductInfo, seller_email=seller_email)

            myproductlisting = ProductListing.objects.filter(product=existing_product).first()

            if not myproductlisting:
                myproductlisting = ProductListing(product=existing_product)
                myproductlisting.save()

            # myproductlisting = ProductListing(product=myproduct)
            # myproductlisting.save()
            return redirect('home/')
    return render(request, "authentication/home.html")

# def viewproduct(request):
#     current_product = request.ProductInfo
#     selleremail = current_product.seller_email
#     name = current_product.product_name
#     price = current_product.product_price
#     description = current_product.product_description
#     quality_tag = current_product.quality_tag
#     category_tag = current_product.category_tag
#     date_posted = current_product.date_posted
#     photo = photo
#     # listing = request.product.listing
#     # img = profile.avatar.url
#     context = { 'selleremail': selleremail, 'name': name, 'price': price, 'description': description, 'quality_tag': quality_tag, 'category_tag': category_tag, 'date_posted': date_posted, 'photo': photo }
#     return render(request, "authentication/home.html", context)

# Backend code

# class Product():
#     def __init__(self, name, price, description, quality_tag, category_tag, seller_name, seller_email, seller_phone, seller_instagram, is_favorited = False):
#         self.name = name
#         self.price = price
#         self.description = description
#         self.quality_tag = QualityTag()
#         self.category_tag = CategoryTag()
#         self.seller_name = seller_name
#         self.seller_email = seller_email
#         self.seller_phone = seller_phone
#         self.seller_instagram = seller_instagram
#         self.is_favorited = is_favorited
#     def get_name(self):
#         return self.name
#     def set_name(self, name):
#         self.name = name
#     def get_price(self):
#         return self.price
#     def set_price(self, price):
#         self.price = price
#     def get_description(self):
#         return self.description
#     def set_description(self, description):
#         self.description = description
#     def get_seller_name(self):
#         return self.seller_name
#     def set_seller_name(self, seller_name):
#         self.seller_name = seller_name
#     def get_seller_email(self):
#         return self.seller_email
#     def set_seller_email(self, seller_email):
#         self.seller_email = seller_email
#     def get_seller_phone(self):
#         return self.seller_phone
#     def set_seller_phone(self, seller_phone):
#         self.seller_phone = seller_phone
#     def get_seller_instagram(self):
#         return self.seller_instagram
#     def set_seller_instagram(self, seller_instagram):
#         self.seller_instagram = seller_instagram
#     def get_is_favorited(self):
#         return self.is_favorited
#     def set_is_favorited(self, is_favorited):
#         self.is_favorited = is_favorited
    
# class QualityTag(Product):
#     productQuality = [
#         ('Like New'),
#         ('Good'),
#         ('Acceptable'),
#     ]
#     def get_quality(Product):
#         return Product.quality_tag
    
#     # will connect this in front end later
#     def set_quality(self, quality):
#         self.quality_tag = quality
    
# class CategoryTag(Product):
#     productCategory = [
#         ('Furniture'),
#         ('Appliances'),
#         ('Textbooks'),
#         ('School supplies'),
#         ('Clothing'),
#         ('Game tickets'),
#     ]
#     def get_category(Product):
#         return Product.category
    
#     def set_category(self, category):
#         self.category = category

# class ProductDirectory(Product):
#     products = [

#     ]

#     def get_product(products, Product):
#         for i in products:
#             if products[i].name == Product.get_name():
#                 return products[i]
            
#     def set_product(products, Product):
#         products[len(products)] = Product