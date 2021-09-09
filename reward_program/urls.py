from django.urls import path, include

urlpatterns = [
    path('', include('reward_program.retailer.urls')),
    path('', include('reward_program.admin.urls'))
]