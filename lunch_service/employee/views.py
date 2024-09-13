from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lunch_service.authentication.models import UserRole
from lunch_service.authentication.permissions import IsCompanyAdmin, IsEmployee

from .serializers import EmployeeSerializer, VoteOneSerializer, VoteThreeSerializer


class CreateEmployeeView(generics.CreateAPIView):
    """
    API view for creating a new employee.
    Access is restricted to users with company admin permissions.
    """
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]  # Ensure the user is authenticated and is a company admin

    def perform_create(self, serializer):
        """
        Custom method to add additional logic during the object creation process.
        Here, it's used to explicitly set the user role to EMPLOYEE upon creation.
        """
        serializer.save(role=UserRole.EMPLOYEE)


class VoteView(generics.CreateAPIView):
    """
    API view for submitting a vote.
    Access is restricted to users with employee permissions.
    This view supports versioning to determine which serializer to use.
    """
    permission_classes = [IsAuthenticated, IsEmployee]  # Ensure the user is authenticated and is an employee

    def get_serializer_class(self):
        """
        Determines which serializer class to use based on the request version.
        If the version is '2.0', it uses the VoteThreeSerializer; otherwise, it defaults to VoteOneSerializer.
        """
        if self.request.version == '2.0':
            return VoteThreeSerializer
        else:
            return VoteOneSerializer
