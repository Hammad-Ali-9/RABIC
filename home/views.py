import os
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from home.models import Signup
from django.contrib.auth import authenticate, login, logout
# Create your views here.

global button_display
global button_styles# Declare global variables to modify
button_display = "display: block;"  # Modify the value
button_styles = "none"

def signup(request):
    error_message = "User already exists with this email."
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        image = request.FILES.get("image")
        # print(image)
        pwd = request.POST.get("pwd")
        
        try:
            user = Signup.objects.get(email=email)
            return render(request, 'signup.html', {'error_message': error_message})
        
        except Signup.DoesNotExist:
            signup = Signup(username=username, email=email, pwd=pwd, image=image, date=datetime.today())
            signup.save()
            return render(request, 'login.html')  

    return render(request, 'signup.html')


def login(request):
  # Modify the value
    error_message = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:  
            user = Signup.objects.get(username=username)
            if user.username==username and user.pwd == password:
                # Signup.objects.all().delete()
                request.session['password'] = user.pwd
                request.session['username'] = user.username       
                request.session['id'] = user.id       
                # image = (user.image.url if user.image else None)
                # print(image+" here is the url")
                return render(request, 'index.html', {'button_styles': button_styles, 'button_display': button_display, 'username': username, 'image': user.image.url})  # Redirect to index page on success
            else:
                error_message="Invalid username or password."
                return render(request, 'login.html', {'error_message': error_message})
        except Signup.DoesNotExist:
            error_message = "Invalid username or password"

    return render(request, "login.html", {'error_message': error_message})

def index(request):     
    id = request.session.get('id')
    if id:
        user=Signup.objects.get(id=id)
        # print(username+" for docs")
        # button_styles = "display: block;"
        return render(request, 'index.html', {'button_styles': button_styles, 'button_display': button_display, 'username': user.username, 'image': user.image}) 
    else:
        return render(request, 'index.html') 

def docs(request):
    id = request.session.get('id')
    if id:
        user=Signup.objects.get(id=id)
        # print(username+" for docs")
        # button_styles = "display: block;"
        return render(request, 'docs.html', {'button_styles': button_styles, 'button_display': button_display, 'username': user.username, 'image': user.image}) 
    else:
        return render(request, 'docs.html') 

def dashboard(request):
    id = request.session.get('id')
    if id:
        user=Signup.objects.get(id=id)
        # print(username+" for docs")
        # button_styles = "display: block;"
        return render(request, 'dashboard.html', {'username': user.username, 'image': user.image}) 
    else:
        return render(request, 'dashboard.html') 
    
def community(request):
    id = request.session.get('id')
    if id:
        user=Signup.objects.get(id=id)
        # print(username+" for docs")
        # button_styles = "display: block;"
        return render(request, 'community.html', {'button_styles': button_styles, 'button_display': button_display, 'username': user.username, 'image': user.image}) 
    else:
        return render(request, 'community.html') 
    
def contact(request):
    id = request.session.get('id')
    if id:
        user=Signup.objects.get(id=id)
        # print(username+" for docs")
        # button_styles = "display: block;"
        return render(request, 'contact.html', {'button_styles': button_styles, 'button_display': button_display, 'username': user.username, 'image': user.image}) 
    else:
        return render(request, 'contact.html') 
# def signup(request):
#     return HttpResponse("Signup page")

# def contact(request):
#     if request.method == "POST":
#         name=request.POST.get("name")
#         email=request.POST.get("email")
#         phone=request.POST.get("phone")
#         address=request.POST.get("address")
#         city=request.POST.get("city")
#         zip=request.POST.get("zip")
#         contact = Contact(
#             name=name,
#             email=email,
#             phone=phone,
#             address=address,
#             city=city,
#             zip=zip,  # Correct variable name
#             date=datetime.today())        
#         contact.save()
        
#     return render(request, 'contact.html')
#     # return HttpResponse("contact page")
