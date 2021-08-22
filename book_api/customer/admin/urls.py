from django.urls import path
from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('customers', views.CustomerListRetrieveViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('customers/<int:pk>/activate', views.ActivateCustomer.as_view()),
    path('customers/<int:pk>/block', views.BlockCustomer.as_view()),
]