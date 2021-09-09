
from employee.employee.views import EmployeeProfile

from django.urls import path

urlpatterns = [
    path('api/profile/employee/', EmployeeProfile.as_view())
]