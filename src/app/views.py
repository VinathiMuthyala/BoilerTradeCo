from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

current_user = "BoilerTradeCo"
# Create your views here.
def home(request):
    return render(request, "authentication/index.html")
    
def signup(request):
    if request.method == "POST":
        # get variable inputs from POST
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        current_user = firstname
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
            
        # check overall length of the email
        length_of_email = len(email)
        if (length_of_email <= 10):
            # raise forms.ValidationError("Email isn't valid.")
            messages.error(request, "Email isn't valid")
        
        # check if email suffix is purdue.edu
        email_suffix = email[-10:]
        if email_suffix != "purdue.edu":
            raise forms.ValidationError("Email is not valid! Please enter a Purdue")
    
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

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'authentication/index.html', {'firstname': firstname})
        # null if user not authenticated
        else:
            messages.error(request, "Username or Password is incorrect!")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    pass

def viewprofile(request):
    name = current_user
    return render(request, "authentication/profile.html", {'name': name})

def settings(request):
    return render(request, "authentication/settings.html")