from django.shortcuts import render, HttpResponse
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
        email=request.POST.get("email")
        pwd=request.POST.get("pwd")
        signup = Signup(email=email,pwd=pwd,date=datetime.today())        
        signup.save()
        
        
    return render(request, 'index.html')
    # return HttpResponse("home page")

# def login(request):
#     return render(request, 'login.html')

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
