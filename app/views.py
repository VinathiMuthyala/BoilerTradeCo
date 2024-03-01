from urllib.parse import urlencode
from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, INFO
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from post_office import mail


users = []
current_number = 0
# Create your views here.
def index(request):
    return render(request, "authentication/index.html")

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
        none = "none"

        user = authenticate(username=email, password=password)
        users.append(user)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'authentication/home.html', {'firstname': firstname})
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
    current_user = request.user
    firstname = current_user.first_name
    lastname = current_user.last_name
    email = current_user.email
    profile = request.user.profile
    img = profile.avatar.url
    context = { 'firstname': firstname, 'lastname': lastname, 'email': email, 'img': img }
    return render(request, "authentication/profile.html", context)

def settings(request):
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

    context = {
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'password_change_form': password_change_form,
    }

    return render(request, "authentication/settings.html", context)

def reportseller(request):
    return render(request, "authentication/report-users.html")

def emailreport(request):
    if request.method == 'POST':
        if 'report_user' in request.POST:
            try:
                print("i got here")
                report_text = request.POST.get('reportText', '')
                seller_email = request.POST.get('sellerEmail', '')
                user_email = request.POST.get('userEmail', '')
                send_mail(subject='User Report: ' + seller_email + "by " + user_email, message=report_text, from_email='neharajamani2004@gmail.com', recipient_list=['boilertradeco@gmail.com'], fail_silently=False)
                #mail.send(recipients=['neharajamani2004@gmail.com'], sender='boilertradeco@gmail.com', subject='User Report: ' + seller_email + "by " + user_email, message=report_text, priority='now')
                report_success = "Report submitted successfully."
                return HttpResponseRedirect(f'/profile/?success_message={report_success}')
            except Exception as e:
                report_fail = "Report was not submitted successfully."
                return HttpResponseRedirect(f'/profile/?error_message={report_fail}')
        else:
            report_fail = "Report was not submitted successfully."
            return HttpResponseRedirect(f'/profile/?error_message={report_fail}')
