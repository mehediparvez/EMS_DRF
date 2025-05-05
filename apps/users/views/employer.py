from rest_framework import permissions, generics
from apps.users.models import Employer
from apps.users.serializers import EmployerSerializer

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class EmployerListCreateView(generics.ListCreateAPIView):
    """View for listing all employers of a user and creating new ones"""
    serializer_class = EmployerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only employers that belong to the current user"""
        return Employer.objects.filter(user=self.request.user)

class EmployerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting specific employers"""
    serializer_class = EmployerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        """Return only employers that belong to the current user"""
        return Employer.objects.filter(user=self.request.user)