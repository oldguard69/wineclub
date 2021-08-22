from django.urls import path, include

urlpatterns = [
    path('', include('publisher.customer.urls')),
    path('', include('publisher.employee.urls'))
]