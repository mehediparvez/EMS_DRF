from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view for Swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Employee Management System",
      default_version='v1',
      description="API Documentation for Employee Management System. For protected endpoints, use JWT token authentication by adding the 'Bearer' prefix before your token in the 'Authorization' header (Example: 'Bearer your_access_token_here').",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@ems.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


class DemoAPIView(APIView):
    def get(self, request):
        data = {
            "message": "Hello, Employee Management System!",
            "status": "success",
            "items": [
                {"id": 1, "name": "Employee 1"},
                {"id": 2, "name": "Employee 2"},
                {"id": 3, "name": "Employee 3"},
            ]
        }
        return Response(data)