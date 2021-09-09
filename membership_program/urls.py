from django.urls import path, include

urlpatterns = [
    path('', include('membership_program.admin.urls')),
    path('', include('membership_program.retailer.urls'))
]