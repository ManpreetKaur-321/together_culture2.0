from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'interests': 'caring'
        }
    
    def test_user_creation(self):
        """Test user creation with custom user model"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=User.MEMBER
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, User.MEMBER)
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_role_choices(self):
        """Test user role choices"""
        user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123',
            role=User.ADMIN
        )
        self.assertEqual(user.role, User.ADMIN)
        self.assertEqual(user.get_role_display(), 'Admin')

class UserLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=User.MEMBER
        )
    
    def test_logout(self):
        """Test user logout"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Test logout
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
