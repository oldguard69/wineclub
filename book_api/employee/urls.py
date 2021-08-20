from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from employee import views


router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]