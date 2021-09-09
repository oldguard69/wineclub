from django.urls import path, include

urlpatterns = [
    path('', include('subscription.admin.urls')),
    path('', include('subscription.retailer.urls'))
]