from django.test import TestCase, Client
from django.urls import reverse
from .models import Signup
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create a test image file
        self.test_image = SimpleUploadedFile(
            name='Vector_1.png',
            content=b'test_image_content',
            content_type='image/png'
        )
        
        # Create a test user with image
        self.test_user = Signup.objects.create(
            username="testuser",
            email="test@example.com",
            pwd="testpassword",
            image=self.test_image,
            date=datetime.today()
        )
        
        # Test data for new signup
        self.signup_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
        }

    def test_signup_page_GET(self):
        """Test that signup page loads correctly"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_POST_success(self):
        """Test successful user registration"""
        # Create a test image file
        image = SimpleUploadedFile(
            name='Vector_1.png',
            content=b'test_image_content',  # Test image content
            content_type='image/png'
        )
        
        # Add image to signup data
        self.signup_data['image'] = image
        
        response = self.client.post(reverse('signup'), self.signup_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
        # Verify user was created
        self.assertTrue(Signup.objects.filter(email='newuser@example.com').exists())

    def test_signup_POST_existing_email(self):
        """Test signup with existing email"""
        self.signup_data['email'] = 'test@example.com'  # Use existing email
        response = self.client.post(reverse('signup'), self.signup_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertContains(response, 'User already exists with this email.')

    def test_login_page_GET(self):
        """Test that login page loads correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_POST_success(self):
        """Test successful login"""
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
        # Check if session variables are set
        self.assertEqual(self.client.session['username'], 'testuser')
        self.assertEqual(self.client.session['password'], 'testpassword')
        self.assertEqual(self.client.session['id'], self.test_user.id)

    def test_login_POST_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password')

    def test_logout(self):
        """Test logout functionality"""
        # First login
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.post(reverse('login'), login_data)
        
        # Then logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
        # Verify session is cleared
        self.assertEqual(dict(self.client.session), {})
