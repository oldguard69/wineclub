from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('business_category.admin.urls')),
    path('', include('business_category.retailer.urls'))
]