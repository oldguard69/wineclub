from django.urls import path, include

urlpatterns = [
    path('', include('customer.admin.urls')),
    path('', include('customer.customer.urls'))
]