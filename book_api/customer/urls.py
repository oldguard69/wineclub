from django.urls import path, include
from rest_framework.routers import DefaultRouter


from customer import views

CustomerListRetrievRouter = DefaultRouter()
CustomerListRetrievRouter.register(r'customers', views.CustomerListRetrieveViewSet)

urlpatterns = [
    path('', include(CustomerListRetrievRouter.urls)),
    path('customers/<int:pk>/activate', views.ActivateCustomer.as_view()),
    path('customers/<int:pk>/block', views.BlockCustomer.as_view()),
    path('customer-profile/', views.CustomerProfile.as_view()),
    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view())
]