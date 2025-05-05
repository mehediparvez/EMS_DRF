from django.urls import path
from apps.users.views import SignUpView, LoginView, LogoutView, ProfileView
from apps.users.views import EmployerListCreateView, EmployerDetailView
from . import views

urlpatterns = [
    path('docs/', views.schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', views.schema_view.with_ui('redoc', cache_timeout=0)),
    
    # Authentication endpoints
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    
    # Employer endpoints
    path('employers/', EmployerListCreateView.as_view(), name='employer-list-create'),
    path('employers/<int:pk>/', EmployerDetailView.as_view(), name='employer-detail'),
]