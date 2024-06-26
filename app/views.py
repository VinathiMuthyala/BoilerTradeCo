from urllib.parse import urlencode
from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Profile, SellerRating
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import base64
import random
import string
from django.urls import reverse
from app2.models import ProductInfo
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RatingForm


# Create your views here.
def index(request):
    return render(request, "authentication/index.html")
    # if request.method == 'POST':
    #     email = request.POST['email']
    #     password = request.POST['password']

    #     user = authenticate(username=email, password=password)

    #     if user is not None:
    #         login(request, user)
    #         firstname = user.first_name

    #         return render(request, 'authentication/home.html', {'firstname': firstname})
    #     else:
    #         print(e)
    #         report_fail = "Report was not submitted successfully."
    #         return HttpResponseRedirect(f'/profile/?error_message={report_fail}')

def home(request):
    return render(request, "authentication/home.html")
    
def signup(request):
    if request.method == "POST":
        # get variable inputs from POST
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        password_conf = request.POST.get('password_conf')

        # check if email already exists
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            error_message = "Email already registered!"
            return HttpResponseRedirect(f'/signup/?error_message={error_message}')
            #return redirect('signup')
            #return render(request, 'signup', {'error_message': "Email already registered!"})

        # check to see if inputted passwords match
        if password and password_conf and password != password_conf:
        #    raise forms.ValidationError("Passwords don't match.")
            messages.error(request, "Passwords don't match.")
            password_error = "Passwords don't match."
            return HttpResponseRedirect(f'/signup/?error_message={password_error}')
            
        # check overall length of the email
        length_of_email = len(email)
        if (length_of_email <= 10):
            # raise forms.ValidationError("Email isn't valid.")
            email_error = "Email isn't valid!"
            return HttpResponseRedirect(f'/signup/?error_message={email_error}')
            messages.error(request, "Email isn't valid")
        
        # check if email suffix is purdue.edu
        email_suffix = email[-10:]
        if email_suffix != "purdue.edu":
            # raise forms.ValidationError("Email is not valid! Please enter a Purdue")
            purdue_error = "Email is not valid! Please enter a Purdue email!"
            return HttpResponseRedirect(f'/signup/?error_message={purdue_error}')
    
        # create and save user locally
        # TODO: when database is situated, must store info in database
        myuser = User.objects.create_user(email, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        # have to deal with the case where user enters a username already in the system
        """
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('signup')
        """
        myuser.save()
        myprofile = Profile(user=myuser)
        myprofile.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')
    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            profile = request.user.profile
            print(profile.confirm)
            if (profile.confirm is False):
                print("im here")
                return redirect('email_auth')
            return redirect('add_listing')
        # null if user not authenticated
        else:
            user_invalid = "Email/Password is incorrect!"
            return HttpResponseRedirect(f'/signin/?error_message={user_invalid}')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('index')

def delete_account(request):
    current_user = request.user
    user = User.objects.get(username = current_user.username)
    user.delete()      
    return redirect('index')

def viewprofile(request):
    if not request.user.is_authenticated:
        return redirect('add_listing')
    current_user = request.user
    firstname = current_user.first_name
    lastname = current_user.last_name
    email = current_user.email
    profile = request.user.profile
    img = profile.avatar.url
    user_products = ProductInfo.objects.filter(seller_email=current_user)
    context = { 'firstname': firstname, 'lastname': lastname, 'email': email, 'img': img, 'user_products': user_products }
    return render(request, "authentication/profile.html", context)

def settings(request):
    if not request.user.is_authenticated:
        return redirect('add_listing')
    current_user = request.user
    firstname = current_user.first_name
    lastname = current_user.last_name
    email = current_user.email

    if request.method == 'POST':
        # check if profile img uploaded
        if 'profile-image-input' in request.FILES:
            new_pfp = request.FILES.get('profile-image-input')
            if new_pfp and new_pfp != current_user.profile.avatar.url:
                current_user.profile.avatar = new_pfp
                current_user.profile.save()
                messages.success(request, "Your changes have been saved successfully.")
            return redirect('settings')

        # Check if the form is for changing the password
        elif 'change_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            # Validate old password before proceeding
            user = authenticate(username=current_user.username, password=old_password)
            if user is None:
                messages.error(request, 'Incorrect current password.')
                #add_message(request, INFO, 'account-change-password')
                return redirect('settings')
            
            # Check if new passwords match
            if new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
                #add_message(request, INFO, 'account-change-password')
                return redirect('settings')
            
            # Change password in the database
            user.set_password(new_password1)
            user.save()

            # Update session to prevent the user from being logged out
            update_session_auth_hash(request, user)

            messages.success(request, 'Your password was successfully updated!')
            #add_message(request, INFO, 'account-change-password')
            return redirect('settings')
       
        # check if form is enabling email notifications
        elif 'email_notifications' in request.POST:
            print("came to email notif")
            if request.POST['email_notifications'] == 'on':
                print("did it come here?")
                try:
                    user_email = request.user.email
                    firstname = request.user.first_name
                    lastname = request.user.last_name
                    user_name = f"{firstname} {lastname}"
                    email_text = f"Hi {user_name},\n\n\tThere is a new product posting in this category: . Go to your account on BoilerTradeCo now to see the new posting!\n\n"
                    send_mail(subject='BoilerTradeCo New Product Notification', message=email_text, from_email='boilertradeco@gmail.com', recipient_list=['boilertradeco@gmail.com', user_email], fail_silently=False)
                    messages.success(request, 'Email notifications enabled!')
                    return redirect('settings')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Email notifications were not enabled!')
                    return redirect('settings')
            else:
                messages.success(request, 'Email notifications disabled!')
                return redirect('settings')
        
        # check if the form is changing user profile info
        else:
            new_firstname = request.POST.get('new_firstname')
            new_lastname = request.POST.get('new_lastname')
            new_email = request.POST.get('new_email')
        
            current_user = request.user

            if new_firstname and new_firstname != current_user.first_name:
                current_user.first_name = new_firstname

            if new_lastname and new_lastname != current_user.last_name:
                current_user.last_name = new_lastname

            if new_email and new_email != current_user.email:
                # FIX HERE - CHECK IF IT IS PURDUE EMAIL AGAIN
                # Check if the new email is unique
                if User.objects.filter(email=new_email).exclude(id=current_user.id).exists():
                    messages.error(request, "The provided email is already in use by another user.")
                    return redirect('settings')
                current_user.email = new_email

            current_user.save()
            messages.success(request, "Your changes have been saved successfully.")
            return redirect('settings')

    password_change_form = PasswordChangeForm(request.user)

    notifications = request.user.profile.notifications
    context = {
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'password_change_form': password_change_form,
        'notifications': notifications,
    }

    return render(request, "authentication/settings.html", context)

def reportseller(request):
    return render(request, "authentication/report-users.html")

def emailreport(request):
    if request.method == 'POST':
        if 'report_user' in request.POST:
            try:
                report_text = request.POST.get('reportText')
                seller_email = request.POST.get('sellerEmail')
                #user_email = request.POST.get('userEmail')
                user_email = request.user.email
                email_text = f"{user_email} submitted a report against seller: {seller_email}.\n\nTheir report is as follows:\n{report_text}"
                send_mail(subject='User Report: ' + seller_email + ' by ' + user_email, message=email_text, from_email='boilertradeco@gmail.com', recipient_list=['boilertradeco@gmail.com'], fail_silently=False)
                #send(subject='User Report: ' + seller_email + ' by ' + user_email, message=report_text, recipient_list=['boilertradeco@gmail.com'])
                report_success = "Report submitted successfully."
                return HttpResponseRedirect(f'/profile/?success_message={report_success}')
            except Exception as e:
                print(e)
                report_fail = "Report was not submitted successfully."
                return HttpResponseRedirect(f'/profile/?error_message={report_fail}')

def emailseller(request):
    if request.method == 'POST':
        if 'email_seller' in request.POST:
            try:
                seller_email = request.POST.get('sellerEmail')
                print("seller email: ", seller_email)
                buyer_email = request.user.email
                #buyer_email = request.POST.get('buyerEmail')
                firstname = request.user.first_name
                lastname = request.user.last_name
                buyer_name = f"{firstname} {lastname}"
                contact = request.POST.get('anotherContact')
                print("contact: ", contact)
                if (contact == '' or contact == 'NA' or contact == 'N/A' or contact == 'n/a' or contact == 'na'):
                    email_text = f"Hi {seller_email},\n\n\tA buyer has expressed interest in your product! To contact this buyer, email {buyer_email}."
                else:
                    email_text = f"Hi {seller_email},\n\n\tA buyer has expressed interest in your product! To contact this buyer, email {buyer_email}. They also have listed another method of contact: {contact}."
                send_mail(subject=f"Product Interest from Buyer: {buyer_name}", 
                          message=email_text, 
                          from_email='boilertradeco@gmail.com', 
                          recipient_list=['boilertradeco@gmail.com', seller_email],
                          fail_silently=False)
                interest_success = "Product interest form submitted successfully."
                return HttpResponseRedirect(f'/addlisting/?success_message={interest_success}')
            except Exception as e:
                print(e)
                interest_fail = "Product interest form was not submitted successfully."
                return HttpResponseRedirect(f'/addlisting/?error_message={interest_fail}')
            return redirect('home')

def generate_pdf(template_src, context_dict):
        # with open('static/logo.png', 'rb') as image_file:
        #     logo_data = base64.b64encode(image_file.read()).decode('utf-8')
        template = get_template(template_src)
        # html2 = render_to_string('authentication/home.html', {'logo_data': logo_data})
        html = template.render(context_dict)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="product_listing.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

def get_pdf(request, *args, **kwargs):
        context = {
            'title': 'Generated PDF Page',
            'content': 'Product Listing',
            'user': request.user
        }
        return generate_pdf('authentication/home.html', context)

def generate_auth_password(length):
    password = string.ascii_letters
    return ''.join(random.choice(password) for _ in range (length))

def email_auth(request):
    if request.method == 'POST':
        inputted_password = request.POST.get('password')
        user_password = request.session.get('user_password')
        if inputted_password != user_password:
            purdue_error = "Inputted password is not correct."
            return HttpResponseRedirect(reverse('email_auth') + f'?error_message={purdue_error}')
        else:
            profile = request.user.profile
            profile.confirm = True
            profile.save()  # Don't forget to save changes
            return redirect('add_listing')
    else:
        # Generates random string combination for password generation
        user_password = generate_auth_password(7)
        request.session['user_password'] = user_password

        try:
            user_name = request.user.first_name
            email_text = f"Hi {user_name},\nThanks for creating an account with BoilerTradeCo! \nYour password is: {user_password}"
            user_email = request.user.email
            send_mail(subject='BoilerTradeCo Authentication Password', message=email_text,
                      from_email='boilertradeco@gmail.com', recipient_list=['boilertradeco@gmail.com', user_email],
                      fail_silently=False)
        except Exception as e:
            print(e)
            # Handle email sending failure here
    return render(request, "authentication/email_auth.html")


# def filter_products_by_price(request):
#     price_range = request.GET.get('priceRange')  # Get the priceRange parameter from the request

#     if price_range is None:
#         return HttpResponseBadRequest("Missing priceRange parameter")

#     try:
#         max_price = int(price_range)  # Maximum price from the slider
#         filtered_products = ProductInfo.objects.filter(price__lte=max_price)

#         products = ([{
#         'name': product.name,
#         'price': product.price,
#         'image': product.image.url,
#         'id': product.pk,
#         } for product in filtered_products])
        
#     except (ValueError, TypeError):
#         return HttpResponseBadRequest("Invalid priceRange parameter")

#     return render(request, 'productdir/filtered-products.html', {'products': products,})


# def filter_products_by_category(request, category_tag):
#     filtered_products = ProductInfo.objects.filter(category_tag__tag=category_tag)

#     products = ([{
#         'name': product.name,
#         'price': product.price,
#         'image': product.image.url,
#         'id': product.pk,
#     } for product in filtered_products])

#     return render(request, 'productdir/filtered-products.html', {
#         'products': products,
#     })



# this is by seller id below

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

def rate_seller(request, seller_email):
    #existing_rating = SellerRating.objects.filter(seller_email=seller_email, user=request.user).last()
    #return render(request, 'authentication/rate_seller.html', {'seller_email': seller_email, 'existing_rating': existing_rating})
    return render(request, 'authentication/rate_seller.html', {'seller_email': seller_email})

def edit_seller(request, seller_email):
    print("LAST RATING BELOW")
    existing_rating = SellerRating.objects.filter(seller_email=seller_email, user=request.user).last()
    if existing_rating:
        print(existing_rating.rating)
        rating = existing_rating.rating
    else:
        rating = 7
    return render(request, 'authentication/edit_seller.html', {'seller_email': seller_email, 'rating': rating, 'comment': existing_rating.comment})

def submit_rating(request):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        seller_email = request.POST.get('seller_email')
        seller = User.objects.get(email=seller_email)
        user = request.user
        SellerRating.objects.create(seller_email=seller_email, seller=seller, user=user, rating=rating, comment=comment)
        update_average_rating(seller)
    return redirect('add_listing')

def update_average_rating(seller):
    all_ratings = SellerRating.objects.filter(seller=seller)
    total_ratings = sum([rating.rating for rating in all_ratings])
    num_ratings = len(all_ratings)
    if num_ratings > 0:
        average_rating = total_ratings / num_ratings
        profile = seller.profile
        profile.average_rating = average_rating
        profile.save()
    if num_ratings == 0:
        average_rating = 0

def rate_edit(request):
    if request.method == 'POST':
        seller_email = request.POST.get('seller_email')
        edit_rating = int(request.POST.get('editRating'))
        edit_comment = request.POST.get('editComment', '')
        seller = User.objects.get(email=seller_email)
        user = request.user

        existing_rating = SellerRating.objects.filter(seller_email=seller_email, user=request.user).last()

        if existing_rating:
            SellerRating.objects.filter(seller_email=seller_email, user=request.user).last().delete()

        SellerRating.objects.create(seller_email=seller_email, seller=seller, user=user, rating=edit_rating, comment=edit_comment)
        update_average_rating(seller)

    return redirect('add_listing')

def delete_rating(request, seller_email):
    rating = SellerRating.objects.filter(seller_email=seller_email, user=request.user).last()
    if rating and rating.user == request.user:
        rating.delete()
    return redirect('add_listing')

# def edit_rating(request):
#     print("HELOOOOOOOOO")
#     print("we in")
#     if request.method == 'POST':
#         print("in post")
#         seller_email = request.POST.get('seller_email')
#         existing_rating = SellerRating.objects.filter(seller_email=seller_email).first()
#         print(existing_rating)

#         if existing_rating:
#             existing_rating.rating = request.POST.get('editRating')
#             existing_rating.comment = request.POST.get('editComment')
#             existing_rating.save()
#             return redirect('rate_seller', seller_email=seller_email)
        
#     return redirect('rate_seller')
               
def update_notifications(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        notifications_disabled = request.POST.get('notifications_disabled')
        print(notifications_disabled)
        if notifications_disabled == 'true':
            print("made notifications false")
            request.user.profile.notifications = False
        else:
            print("made notifications true")
            request.user.profile.notifications = True
        request.user.profile.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'}, status=400)

