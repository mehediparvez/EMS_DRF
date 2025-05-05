from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.models import Employer
from apps.users.serializers import EmployerSerializer
from apps.users.views import EmployerListCreateView, EmployerDetailView

User = get_user_model()


class EmployerViewTestCase(TestCase):
    """
    Base test case for employer views with common setup
    """
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPassword123!'
        )
        
        # Create test user 2
        self.user2 = User.objects.create_user(
            email='test2@example.com',
            name='Test User 2',
            password='TestPassword123!'
        )
        
        # Create a test employer for the user
        self.employer = Employer.objects.create(
            user=self.user,
            company_name='Test Company',
            contact_person_name='Test Contact',
            email='company@example.com',
            phone_number='1234567890',
            address='123 Test Street, Test City'
        )
        
        # Create a test employer for user2
        self.employer2 = Employer.objects.create(
            user=self.user2,
            company_name='Test Company 2',
            contact_person_name='Test Contact 2',
            email='company2@example.com',
            phone_number='9876543210',
            address='456 Test Avenue, Test City'
        )
        
        # Setup test client
        self.client = APIClient()
        
        # Employer test data
        self.valid_employer_data = {
            'company_name': 'New Test Company',
            'contact_person_name': 'New Contact',
            'email': 'new@example.com',
            'phone_number': '5555555555',
            'address': '789 New Street, New City'
        }
        
        # URL endpoints
        self.employer_list_url = reverse('employer-list-create')
        self.employer_detail_url = reverse('employer-detail', kwargs={'pk': self.employer.id})
        self.employer2_detail_url = reverse('employer-detail', kwargs={'pk': self.employer2.id})


class EmployerListCreateViewTests(EmployerViewTestCase):
    """
    Test cases for EmployerListCreateView (listing and creating employers)
    """
    def test_list_employers_authenticated(self):
        """Test that an authenticated user can list their employers"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.employer_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # User should only see their own employer
        self.assertEqual(response.data[0]['company_name'], 'Test Company')
    
    def test_list_employers_unauthenticated(self):
        """Test that unauthenticated users cannot list employers"""
        response = self.client.get(self.employer_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_employer_authenticated(self):
        """Test that an authenticated user can create a new employer"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.employer_list_url,
            self.valid_employer_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employer.objects.count(), 3)
        self.assertEqual(Employer.objects.filter(user=self.user).count(), 2)
        
        # Verify the created employer
        new_employer = Employer.objects.get(company_name='New Test Company')
        self.assertEqual(new_employer.user, self.user)
        self.assertEqual(new_employer.email, 'new@example.com')
    
    def test_create_employer_unauthenticated(self):
        """Test that unauthenticated users cannot create employers"""
        response = self.client.post(
            self.employer_list_url,
            self.valid_employer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Employer.objects.count(), 2)


class EmployerDetailViewTests(EmployerViewTestCase):
    """
    Test cases for EmployerDetailView (retrieve, update, delete specific employers)
    """
    def test_get_own_employer(self):
        """Test that a user can retrieve their own employer"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.employer_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], 'Test Company')
        self.assertEqual(response.data['email'], 'company@example.com')
    
    def test_get_other_user_employer(self):
        """Test that a user cannot retrieve another user's employer"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.employer2_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_own_employer(self):
        """Test that a user can update their own employer"""
        self.client.force_authenticate(user=self.user)
        update_data = {
            'company_name': 'Updated Company',
            'contact_person_name': 'Updated Contact',
            'email': 'updated@example.com',
            'phone_number': '1234567890',
            'address': '123 Test Street, Test City'
        }
        
        response = self.client.put(
            self.employer_detail_url,
            update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the employer was updated
        self.employer.refresh_from_db()
        self.assertEqual(self.employer.company_name, 'Updated Company')
        self.assertEqual(self.employer.email, 'updated@example.com')
    
    def test_partial_update_own_employer(self):
        """Test that a user can partially update their own employer"""
        self.client.force_authenticate(user=self.user)
        partial_update = {
            'company_name': 'Partially Updated Company'
        }
        
        response = self.client.patch(
            self.employer_detail_url,
            partial_update,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify partial update
        self.employer.refresh_from_db()
        self.assertEqual(self.employer.company_name, 'Partially Updated Company')
        self.assertEqual(self.employer.email, 'company@example.com')
    
    def test_delete_own_employer(self):
        """Test that a user can delete their own employer"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.employer_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employer.objects.filter(id=self.employer.id).count(), 0)
        self.assertEqual(Employer.objects.count(), 1)
    
    def test_unauthorized_operations(self):
        """Test that unauthenticated users cannot perform any operations"""
        # GET
        response = self.client.get(self.employer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # PUT
        response = self.client.put(
            self.employer_detail_url,
            self.valid_employer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # PATCH
        response = self.client.patch(
            self.employer_detail_url,
            {'company_name': 'Updated Name'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # DELETE
        response = self.client.delete(self.employer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Employer.objects.count(), 2)