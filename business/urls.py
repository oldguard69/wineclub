from django.urls import path, include

urlpatterns = [
    path('', include('business.admin.urls')),
    path('', include('business.retailer.urls'))
]