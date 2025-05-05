from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from apps.users.models.employer import Employer
from apps.users.serializers.employer_serializer import EmployerSerializer

User = get_user_model()

class EmployerSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPassword123!'
        )
        
        self.employer_data = {
            'company_name': 'Test Company',
            'contact_person_name': 'John Doe',
            'email': 'contact@testcompany.com',
            'phone_number': '1234567890',
            'address': '123 Test Street, Test City'
        }
        
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user
        
        self.employer = Employer.objects.create(
            user=self.user,
            company_name='Existing Company',
            contact_person_name='Jane Smith',
            email='contact@existingcompany.com',
            phone_number='0987654321',
            address='456 Existing Street, Existing City'
        )

    def test_employer_serializer_read(self):
        """Test that EmployerSerializer returns expected fields"""
        serializer = EmployerSerializer(instance=self.employer)
        data = serializer.data
        
        self.assertEqual(set(data.keys()), {'id', 'company_name', 'contact_person_name', 
                                          'email', 'phone_number', 'address', 'created_at'})
        self.assertEqual(data['company_name'], self.employer.company_name)
        self.assertEqual(data['contact_person_name'], self.employer.contact_person_name)
        self.assertEqual(data['email'], self.employer.email)
        self.assertEqual(data['phone_number'], self.employer.phone_number)
        self.assertEqual(data['address'], self.employer.address)
    
    def test_employer_serializer_create(self):
        """Test that EmployerSerializer creates an employer correctly with current user"""
        serializer = EmployerSerializer(data=self.employer_data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        
        employer = serializer.save()
        self.assertEqual(employer.company_name, self.employer_data['company_name'])
        self.assertEqual(employer.contact_person_name, self.employer_data['contact_person_name'])
        self.assertEqual(employer.email, self.employer_data['email'])
        self.assertEqual(employer.phone_number, self.employer_data['phone_number'])
        self.assertEqual(employer.address, self.employer_data['address'])
        
        self.assertEqual(employer.user, self.user)
    
    def test_employer_serializer_validation(self):
        """Test that EmployerSerializer validates required fields"""

        invalid_data = {
            'company_name': 'Test Company',
            'email': 'contact@testcompany.com'
        }
        serializer = EmployerSerializer(data=invalid_data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('contact_person_name', serializer.errors)
        self.assertIn('phone_number', serializer.errors)
        self.assertIn('address', serializer.errors)