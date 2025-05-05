from django.urls import path
from apps.users.views.auth import SignUpView, ProfileView

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('', ProfileView.as_view(), name='profile'),
]