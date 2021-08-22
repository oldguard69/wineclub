from django.urls import path, include



urlpatterns = [
    path('', include('book.employee.urls')),
    path('', include('book.customer.urls'))
]