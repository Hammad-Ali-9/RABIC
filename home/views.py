from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from home.models import Signup
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
        signup = Signup(username=username,email=email,pwd=pwd,date=datetime.today())        
        signup.save()   
        
    return render(request, 'index.html')


def login(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(username=username)
            if user.pwd == password:
                request.session['password'] = user.pwd
                request.session['username'] = user.username
                return render(request, 'index.html')  # Redirect to index page on success
            else:
                error_message = "Invalid username or password"
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
