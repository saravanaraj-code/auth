from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Employee
from .serializers import RegisterSerializer, EmployeeSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create an Employee instance for the user
        employee_data = {
            "user": user.pk,
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "phone_number": request.data.get("phone_number"),
        }
        employee_serializer = EmployeeSerializer(data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
        else:
            # Handle validation errors for the employee data
            user.delete()  # Rollback user creation if employee creation fails
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
