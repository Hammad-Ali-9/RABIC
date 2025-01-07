import os
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from home.models import Signup, CommunityPost, Tag, Category
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json
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
        
        # Add FAQ questions list
        faq_questions = [
            "How do I link a data source?",
            "Can I analyze spreadsheets with multiple tabs?",
            "What do I do after linking a data source?",
            "Is there a discount for students, professors, or teachers?",
            "What can I do in RABIc?",
            "What data sources and file formats does RABIc support?"
        ]
        
        context = {
            'button_styles': button_styles,
            'button_display': button_display,
            'username': user.username if user else None,
            'image': user.image if user else None,
            'faq_questions': faq_questions  # Add this to the context
        }
        
        return render(request, 'docs.html', context)
    else:
        return render(request, 'docs.html') 

def dashboard(request):
    id = request.session.get('id')
    if id:
        user = Signup.objects.get(id=id)
        
        # Calculate stats
        total_requests = CommunityPost.objects.filter(Signup=user).count()
        
        # Get user's posts with their timestamps
        user_posts = CommunityPost.objects.filter(Signup=user).order_by('-activity_time')
        
        # Calculate time spent (dummy data - you'll need to implement actual tracking)
        time_spent_hours = 12
        last_active = user_posts.first().activity_time if user_posts.exists() else "No activity"
        
        # Get recent login history
        recent_logins = [
            {"date": timezone.now() - timedelta(days=i), "time": "09:00 AM"}
            for i in range(5)
        ]
        
        # Generate chart data (last 7 days activity)
        today = timezone.now().date()
        chart_labels = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        chart_data = [
            CommunityPost.objects.filter(
                Signup=user,
                activity_time__date=today - timedelta(days=i)
            ).count()
            for i in range(6, -1, -1)
        ]
        
        # Get recent activities
        recent_activities = []
        for post in user_posts[:5]:
            recent_activities.append({
                'type': 'post',
                'description': f'Created post: {post.topic}',
                'timestamp': post.activity_time
            })

        context = {
            'username': user.username,
            'email': user.email,
            'image': user.image,
            'total_requests': total_requests,
            'request_trend': 15,  # Dummy data
            'time_spent_hours': time_spent_hours,
            'last_active': last_active,
            'total_reactions': 42,  # Dummy data
            'likes': 30,  # Dummy data
            'comments': 12,  # Dummy data
            'recent_logins': recent_logins,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': chart_data,
            'recent_activities': recent_activities,
            # Add these to control button visibility
            'button_styles': 'none',  # Hide login/signup
            'button_display': 'display: block;'  # Show user dropdown
        }
        
        return render(request, 'dashboard.html', context)
    else:
        return redirect('login')

def submit_post(request):
    if request.method == 'POST':
        try:
            # Get form data
            topic = request.POST.get('topic')
            category_name = request.POST.get('category')
            content = request.POST.get('content')
            tags_input = request.POST.get('tags', '')

            # Get category (must exist from dropdown)
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                # Fallback to General category
                category = Category.objects.get_or_create(name="General")[0]

            # Get the user
            user_signup = Signup.objects.get(id=request.session['id'])

            # Create the post
            post = CommunityPost.objects.create(
                topic=topic,
                category=category,
                content=content,
                Signup=user_signup
            )

            # Handle tags
            if tags_input:
                tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            return redirect('community')
        except Exception as e:
            print(f"Error in submit_post: {e}")
            return redirect('community')

    return redirect('community')

    
def community(request):
    try:
        # Get all posts initially
        posts = CommunityPost.objects.all()

        # Filter by category
        category_filter = request.GET.get('category')
        if category_filter:
            posts = posts.filter(category__name=category_filter)

        # Filter by tag
        tag_filter = request.GET.get('tag')
        if tag_filter:
            posts = posts.filter(tags__name=tag_filter)

        # Sort by top (most views) or latest
        sort = request.GET.get('sort')
        if sort == 'top':
            posts = posts.order_by('-views')
        else:
            posts = posts.order_by('-activity_time')

        # Get all categories and tags for the dropdowns
        categories = Category.objects.all()
        all_tags = Tag.objects.all()

        # Get user info for the navbar
        id = request.session.get('id')
        user = Signup.objects.get(id=id) if id else None

        context = {
            'posts': posts,
            'categories': categories,
            'all_tags': all_tags,
            'button_styles': button_styles,
            'button_display': button_display,
        }
        
        if user:
            context.update({
                'username': user.username,
                'image': user.image
            })

        return render(request, 'community.html', context)
    except Exception as e:
        print(f"Error in community view: {e}")
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

def community_view(request):
    # Get all posts initially
    posts = CommunityPost.objects.all()

    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        posts = posts.filter(category=category_filter)

    # Filter by tag
    tag_filter = request.GET.get('tag')
    if tag_filter:
        posts = posts.filter(tags__name=tag_filter)

    # Sort by top (most views)
    sort = request.GET.get('sort')
    if sort == 'top':
        posts = posts.order_by('-views')
    else:
        posts = posts.order_by('-activity_time')

    # Get all categories and tags for the dropdowns
    categories = Category.objects.all()
    all_tags = Tag.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'all_tags': all_tags,
    }
    return render(request, 'community.html', context) 

def rabic_bot(request):
    id = request.session.get('id')
    context = {}
    
    if id:
        try:
            user = Signup.objects.get(id=id)
            context = {
                'button_styles': button_styles,
                'button_display': button_display,
                'username': user.username,
                'image': user.image.url if user.image else None,  # Handle case when image might not exist
                'is_authenticated': True
            }
        except Signup.DoesNotExist:
            # Handle case when user doesn't exist
            request.session.flush()
            context = {'is_authenticated': False}
    else:
        context = {'is_authenticated': False}
    
    return render(request, 'rabic_bot.html', context) 