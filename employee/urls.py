from django.urls import path, include

urlpatterns = [
    path('', include('employee.employee.urls'))
]