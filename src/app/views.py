from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 

# Create your views here.
def home(request):
    return render(request, "app/index.html")

    
def signup(request):
    if request.method == "POST":
        # get variable inputs from POST
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        password_conf = request.POST.get('password_conf')

        # check to see if inputted passwords match
        if password and password_conf and password != password_conf:
            raise forms.ValidationError("Passwords don't match.")
        
        # check overall length of the email
        length_of_email = len(email)
        if (length_of_email <= 10):
            raise forms.ValidationError("Email isn't valid.")
        
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
    return render(request, "app/signup.html")


def signin(request):
    return render(request, "app/signin.html")

def signout(request):
    pass