from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import models
from datetime import date
from django.contrib import messages
from django.core.serializers import serialize
from .models import ProductInfo, CategoryTag, QualityTag, ProductListing, Bookmark
from django.conf import settings
import os, json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from .forms import NewProductForm, EditProductForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

# Create your views here.
def layout(request):
    return render(request, 'authentication/light-dark-toggle.html') # confirm if this is okay productdir/index.html before

def add_product(request):
    return render(request, 'productdir/add-product.html')

def add_listing(request):
    print("Inside add_listing")
    products = ProductInfo.objects.filter(is_sold=False)
    print("Number of products:", len(products))
    categories = CategoryTag.objects.all().values('tag')
    # print(categories)
    qualities = QualityTag.objects.all().values('tag')

    # product_list_json = serialize('json', products)

    products = ([{
        'name': product.name,
        'price': product.price,
        'image': product.image.url,
        'quality_tag': product.quality_tag,
        'category_tag': product.category_tag,
        'id': product.pk,
    } for product in products])

    print("Products", products)

    # product_list = ([{
    #     'price': products.price,
    #     'product': products.name,
    # }])

    # print("JSON", product_list)

    # product_list_json = json.dumps(product_list)

    # category_list = list(categories)
    # quality_list = list(qualities)

    # return JsonResponse({'products': product_list, 'categories': category_list, 'qualities': quality_list})

    return render(request, 'productdir/sample-directory.html', {
        # 'products_json': products_json
        'products' : products,
        'categories' : categories,
        'qualities' : qualities,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller_email = request.user
            product.save()
            category = product.category_tag
            seller_email = product.seller_email
            product_name = product.name
            product_price = product.price
            quality = product.quality_tag
            user_email = request.user.email
            firstname = request.user.first_name
            lastname = request.user.last_name
            user_name = f"{firstname} {lastname}"
            email_text = f"Hi {user_name},\n\n\tThere is a new product posting in this category: {category}.\n\nProduct details:\n\tSeller email: {seller_email}\n\tProduct name: {product_name}\n\tProduct price: ${product_price}\n\tQuality: {quality}\n\nGo to your account on BoilerTradeCo now to see the new posting!"
            send_mail(subject='BoilerTradeCo New Product Notification', message=email_text, from_email='boilertradeco@gmail.com', recipient_list=['boilertradeco@gmail.com', user_email], fail_silently=False)
            return redirect("/addlisting")
    else:
        form = NewProductForm()
    return render(request, 'productdir/form.html', {
        'form': form,
        'title': 'Add a Product!',
        'is_sold_option': False,
        'current_seller_email': request.user,
    })

@login_required
def edit(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("/addlisting")
    else:
        form = EditProductForm(instance=product)
    return render(request, 'productdir/form.html', {
        'form': form,
        'title': 'Edit Product Posting!',
        'is_sold_option': True,
    })

@login_required
def delete(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk)
    product.delete()

    return redirect('/addlisting/')

# def editproduct(request):
#     if request.method == 'POST':
#         if 'edit_product' in request.POST:
#             product_name = request.POST.get('productName')
#             product_price = request.POST.get('productPrice')
#             product_description = request.POST.get('productDescription')
#             quality_tag = request.POST.get('qualityTag')
#             category_tag = request.POST.get('categoryTag')
#             #user_email = request.user.email
#             return redirect('home')

def detail(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk)
    current_user = request.user
    email = current_user.email
    firstname = current_user.first_name
    productname = product.name
    print(current_user)
    print(email)
    print("Seller email", product.seller_email)

    id = product.product_id
    print(id)

    return render(request, 'authentication/detail.html', {
        'product': product,
        'email': email,
        'user': current_user,
        'id': id,
        'firstname': firstname,
        'productname': productname,
    })

def filter_products_by_category(request, category_tag):
    filtered_products = ProductInfo.objects.filter(category_tag__tag=category_tag)
    print("CATEGORY TAG IS:", category_tag)

    products = ([{
        'name': product.name,
        'price': product.price,
        'image': product.image.url,
        'id': product.pk,
    } for product in filtered_products])

    return render(request, 'productdir/filtered-products.html', {
        'products': products,
    })

def filter_products_by_quality(request, quality_tag):
    # quality_tag = quality_tag.replace('-', ' ')

    filtered_products = ProductInfo.objects.filter(quality_tag__tag=quality_tag)

    print("QUALITY TAG IS:", quality_tag)

    products = ([{
        'name': product.name,
        'price': product.price,
        'image': product.image.url,
        'id': product.pk,
    } for product in filtered_products])

    return render(request, 'productdir/filtered-products.html', {
        'products': products,
    })

def generate_bookmarks(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'error_message': 'User not authenticated'}, status=401)

    # Retrieve the bookmarked products for the current user
    bookmarked_products = Bookmark.objects.filter(user=request.user)

    # Extract the product IDs from the bookmarked products
    product_ids = [bookmark.post.product_id for bookmark in bookmarked_products]

    # Retrieve the actual product objects using the IDs
    products = ProductInfo.objects.filter(pk__in=product_ids)

    return render(request, 'productdir/bookmarks.html', {'bookmarked_products': products})

@require_POST
def bookmark_product(request):
    print("im here right now")
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    # Get the product ID from the AJAX request
    product_id = request.POST.get('product_id')

    # Check if the product ID is valid
    if not product_id:
        return JsonResponse({'error': 'Invalid product ID'}, status=400)

    try:
        product_id = int(product_id)  # Convert to integer
    except ValueError:
        return JsonResponse({'error': 'Invalid product ID'}, status=400)

    # Check if the product exists
    try:
        product = ProductInfo.objects.get(pk=product_id)
    except ProductInfo.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    # Check if the product is already bookmarked by the user
    if Bookmark.objects.filter(user=request.user, post_id=product_id).exists():
        return JsonResponse({'error': 'Product already bookmarked'}, status=400)

    # Create a new bookmark entry
    bookmark = Bookmark(user=request.user, post_id=product_id)
    bookmark.save()

    # Return success response
    return JsonResponse({'success': 'Product bookmarked successfully'})


# def rate_seller(request, seller_id):
#     if request.method == 'POST':
#         rating = int(request.POST.get('rating'))
#         comment = request.POST.get('comment')
#         seller = User.objects.get(pk=seller_id)
#         user = request.user
#         SellerRating.objects.create(seller=seller, user=user, rating=rating, comment=comment)
#         update_average_rating(seller)
#         return redirect('seller_profile', seller_id=seller_id)
#     return render(request, 'rate_seller.html')

# def update_average_rating(seller):
#     all_ratings = SellerRating.objects.filter(seller=seller)
#     total_ratings = sum([rating.rating for rating in all_ratings])
#     num_ratings = len(all_ratings)
#     if num_ratings > 0:
#         average_rating = total_ratings / num_ratings
#         profile = seller.profile
#         profile.average_rating = average_rating
#         profile.save()



# def add_listing(request):
#     print("printing product info from views.py")
#     if request.method == "POST":
#         if request.FILES.get('photo'):
#             photo = request.FILES['photo']
#             if photo.content_type.startswith('image'):
#                 if photo.size <= 800 * 1024:  # 800 KB in bytes
#                     save_path = os.path.join(settings.MEDIA_ROOT, 'photos', photo.name)
#                     with open(save_path, 'wb') as destination:
#                         for chunk in photo.chunks():
#                             destination.write(chunk)
#                 else:
#                     error_message = "File size exceeds the maximum allowed size (800KB). Please choose a smaller file."
#                     messages.MessageFailure(error_message)
#             else:
#                 error_message = "Invalid file type. Please upload an image (JPG, PNG, GIF)."
#                 messages.MessageFailure(error_message)
#         else:
#             error_message = "No file uploaded."
#             messages.MessageFailure(error_message)
#         if 'product_info' in request.POST:
#             seller_email = request.POST.get('sellerEmail')
#             product_name = request.POST.get('productName')
#             product_price = request.POST.get('productPrice')
#             product_description = request.POST.get('productDescription')
#             quality_tag = request.POST.get('qualityTag')
#             category_tag = request.POST.get('categoryTag')
#             date_posted = date.today().strftime("%Y-%m-%d")
#             # img = photo
#             print(product_name)
#             print(product_price)
#             print(seller_email)
#             print(product_description)
#             print(quality_tag)
#             print(category_tag)
#             print("the date: ", date_posted)

#             myproduct = ProductInfo.create_product(
#                 seller_email=seller_email,
#                 name=product_name,
#                 price=product_price,
#                 description=product_description,
#                 quality_tag=quality_tag,
#                 category_tag=category_tag,
#                 date_posted=date_posted,
#                 # photo=photo
#             )
#             # myproduct = ProductInfo.create_product(product_name, product_price, seller_email, product_description, quality_tag, category_tag, date_posted)
#             #myproduct = ProductInfo(name=product_name, price=product_price, seller_email = seller_email, description=product_description, quality_tag=quality_tag, category_tag=category_tag, date_posted = date_posted)
#             # myproduct.save()

#             existing_product = get_object_or_404(ProductInfo, seller_email=seller_email)

#             myproductlisting = ProductListing.objects.filter(product=existing_product).first()

#             if not myproductlisting:
#                 myproductlisting = ProductListing(product=existing_product)
#                 myproductlisting.save()

#             # myproductlisting = ProductListing(product=myproduct)
#             # myproductlisting.save()
#             return redirect('home/')
#     return render(request, "authentication/home.html")

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