from django.urls import path, include


urlpatterns = [
    path('', include('author.employee.urls')),
    path('', include('author.customer.urls')),
]