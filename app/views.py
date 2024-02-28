from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

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
        #current_number = int(current_number) + 1

        # print("check: " + str(user.is_authenticated))

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

def viewprofile(request):
    current_user = request.user
    username = current_user.id
    context = { 'username': username}
    return render(request, "authentication/profile.html", context)

def settings(request):
    return render(request, "authentication/settings.html")
