from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from home.models import Signup
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    # context = {
    #     "name":"hammad",
    #     "section":"5B"
    # }
    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        pwd=request.POST.get("pwd")
        signup = authenticate(username=username,email=email,pwd=pwd,date=datetime.today())        
        signup.save()   
        
    return render(request, 'index.html')


def signup(request):
    error_message = "User already exists with this email."
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        pwd = request.POST.get("pwd")
        
        try:
            user = Signup.objects.get(email=email)
            return render(request, 'signup.html', {'error_message': error_message})
        
        except Signup.DoesNotExist:
            signup = Signup(username=username, email=email, pwd=pwd, date=datetime.today())
            signup.save()
            return render(request, 'login.html')  

    return render(request, 'signup.html')


def login(request):
    button_display="block"
    button_styles="display: none;"
    error_message = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(username=username)
            if user.pwd == password:
                request.session['password'] = user.pwd
                request.session['username'] = user.username
                print(username)
                
                return render(request, 'index.html', {'button_styles': button_styles, 'button_display': button_display, 'username': username})  # Redirect to index page on success
            else:
                error_message="Invalid username or password."
                return render(request, 'login.html', {'error_message': error_message})
        except Signup.DoesNotExist:
            error_message = "Invalid username or password"

    return render(request, "login.html", {'error_message': error_message})

def docs(request):
    return render(request, 'docs.html')

def community(request):
    return render(request, 'community.html')
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
