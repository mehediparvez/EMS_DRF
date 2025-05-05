from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.views.auth import SignUpView, LoginView, LogoutView

User = get_user_model()


class LoginViewTests(TestCase):
    """Tests for the user login functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPassword123!'
        )
        
        self.valid_credentials = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        
        self.invalid_credentials = {
            'email': 'test@example.com',
            'password': 'WrongPassword123!'
        }
        
        self.nonexistent_user = {
            'email': 'nonexistent@example.com',
            'password': 'TestPassword123!'
        }

    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        response = self.client.post(
            self.login_url,
            self.valid_credentials,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            self.login_url,
            self.invalid_credentials,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid Credentials')
    
    def test_login_nonexistent_user(self):
        """Test login with nonexistent user"""
        response = self.client.post(
            self.login_url,
            self.nonexistent_user,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid Credentials')
    
    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post(
            self.login_url,
            {'email': 'test@example.com'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTests(TestCase):
    """Tests for the user logout functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('logout')
        
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPassword123!'
        )
        
        # Generate refresh token for the user
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = self.refresh_token.access_token

    def test_logout_successful(self):
        """Test successful logout"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(
            self.logout_url,
            {'refresh': str(self.refresh_token)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Successfully logged out.')
        
        # Verify token is blacklisted by trying to use it again
        response = self.client.post(
            self.logout_url,
            {'refresh': str(self.refresh_token)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid token.')
    
    def test_logout_no_token(self):
        """Test logout without providing refresh token"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(
            self.logout_url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout_invalid_token(self):
        """Test logout with invalid refresh token"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(
            self.logout_url,
            {'refresh': 'invalid-token'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid token.')
    
    def test_logout_unauthenticated(self):
        """Test logout without authentication"""
        response = self.client.post(
            self.logout_url,
            {'refresh': str(self.refresh_token)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterViewTests(TestCase):
    """Tests for the user registration functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('signup')
        self.valid_payload = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!'
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'TestPassword123!',
            'password2': 'DifferentPassword123!'
        }
        self.incomplete_payload = {
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!'
        }

    def test_register_valid_user(self):
        """Test registering a user with valid data"""
        response = self.client.post(
            self.register_url,
            self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
        self.assertEqual(User.objects.get().name, 'Test User')
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User registered successfully')

    def test_register_invalid_passwords(self):
        """Test registering a user with mismatched passwords"""
        response = self.client.post(
            self.register_url,
            self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_incomplete_data(self):
        """Test registering a user with incomplete data"""
        response = self.client.post(
            self.register_url,
            self.incomplete_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_duplicate_email(self):
        """Test registering a user with an email that already exists"""

        User.objects.create_user(
            email='test@example.com',
            name='Existing User',
            password='ExistingPass123!'
        )
        
        response = self.client.post(
            self.register_url,
            self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)