from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/admin/wine', views.WineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/business/<int:pk>/wine/', views.WineOfABusiness.as_view())
]