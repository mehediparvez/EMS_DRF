from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model to be inherited by other models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'users'
