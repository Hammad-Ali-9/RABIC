import os
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from home.models import Signup, CommunityPost, Tag
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
        pwd = request.POST.get("password")
        
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
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, "login.html")

def logout(request):
    request.session.flush()
    return render(request, 'index.html')

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
 

def submit_post(request):
    if request.method == 'POST':
        # Retrieve data from the form
        topic = request.POST.get('topic')
        category = request.POST.get('category')
        content = request.POST.get('content')
        tags_input = request.POST.get('tags', '')

        # Retrieve the Signup instance for the logged-in user using session['id']
        try:
            user_signup = Signup.objects.get(id=request.session['id'])  # Get the Signup instance using the stored session ID
        except Signup.DoesNotExist:
            # Handle case where no Signup instance is found
            return redirect('error_page')  # Or handle it in a way that suits your logic

        # Create a new CommunityPost and associate it with the Signup instance
        post = CommunityPost.objects.create(
            topic=topic,
            category=category,
            content=content,
            Signup=user_signup  # Assign the Signup instance to the post
        )

        # Handle tags if they were provided
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tags:
                # Get or create the tag in the Tag model
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # Add the tag to the post
                post.tags.add(tag)

        # Redirect to the community page or another page after saving
        return redirect('community')  # Adjust to your view name

    # If not a POST request, render the form to submit the post
    return render(request, 'community.html')

    
def community(request):
    try:
        id = request.session.get('id')
        posts = CommunityPost.objects.all().order_by('-activity_time') 
        
        user=Signup.objects.get(id=id)
        return render(request, 'community.html', {'button_styles': button_styles, 'button_display': button_display, 'username': user.username, 'image': user.image, 'posts': posts}) 
    except:
        return render(request, 'community.html')

def contact(request):
    id = request.session.get('id')
    if id:
        user=Signup.objects.get(id=id)
        
        # We will implemet lists here to store data in it for the sorting and displaying in the coomunity table
        
        # print(username+" for docs")
        # button_styles = "display: block;"
        return render(request, 'contact.html', {'button_styles': button_styles, 'button_display': button_display, 'username': user.username, 'image': user.image}) 
    else:
        return render(request, 'contact.html') 