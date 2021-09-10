from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('api/customer/business', views.BusinessViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/customer/favorite-business/', views.FavoriteBusinessList.as_view()),
    path('api/customer/favorite-business/<int:pk>/', views.FavoriteBusinessAddRemove.as_view()),
]