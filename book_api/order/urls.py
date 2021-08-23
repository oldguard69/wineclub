from django.urls import path, include

urlpatterns = [
    path('', include('order.customer.urls'))
]