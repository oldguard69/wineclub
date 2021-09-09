from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/admin/tourism-pass', views.TourismPassViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/winery/<int:pk>/tourism-pass', views.TourismPassOfAWinery.as_view())
]