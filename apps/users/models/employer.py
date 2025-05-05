from django.db import models
from django.conf import settings
from apps.users.models.base import BaseModel


class Employer(BaseModel):
    """
    Model to represent an employer in the system.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='employers'
    )
    company_name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    class Meta:
        app_label = 'users'
        verbose_name = 'employer'
        verbose_name_plural = 'employers'

    def __str__(self):
        return str(self.company_name)