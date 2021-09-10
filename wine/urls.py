from django.urls import path, include

urlpatterns = [
    path('', include('wine.retailer.urls')),
    path('', include('wine.admin.urls')),
    path('', include('wine.customer.urls'))
]