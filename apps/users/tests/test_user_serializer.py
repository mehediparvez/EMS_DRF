from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.serializers.user_serializer import UserSerializer, UserDetailSerializer

User = get_user_model()

class UserSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!'
        }
        self.user = User.objects.create_user(
            email='existing@example.com',
            name='Existing User',
            password='ExistingPass123!'
        )

    def test_user_serializer_validation(self):
        """Test that UserSerializer validates correctly"""
        # Test valid data
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        
        # Test password mismatch
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'DifferentPassword123!'
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        
        # Test missing required fields
        invalid_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password2', serializer.errors)
        self.assertIn('name', serializer.errors)
    
    def test_user_serializer_create(self):
        """Test that UserSerializer creates a user correctly"""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        
        # Ensure password2 field is not saved to database
        self.assertFalse(hasattr(user, 'password2'))
    
    def test_user_detail_serializer(self):
        """Test that UserDetailSerializer returns expected fields"""
        serializer = UserDetailSerializer(instance=self.user)
        data = serializer.data
        
        self.assertEqual(set(data.keys()), {'id', 'email', 'name', 'date_joined'})
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['name'], self.user.name)