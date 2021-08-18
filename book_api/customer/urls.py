from django.urls import path

from customer import views

urlpatterns = [
    path('customer/', views.CustomerList.as_view()),
    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view())
]