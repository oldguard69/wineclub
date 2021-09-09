from django.urls import path, include

urlpatterns = [
    path('', include('tourism_pass.retailer.urls')),
    path('', include('tourism_pass.admin.urls'))
]