from django.urls import path, include

urlpatterns = [
    path('', include('genre.customer.urls')),
    path('', include('genre.employee.urls'))
]