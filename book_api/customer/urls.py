from django.urls import path

from customer import views

urlpatterns = [path('customer/', views.CustomerList.as_view())]