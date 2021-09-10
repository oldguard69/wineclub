from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('api/customer/wine', views.WineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/customer/favorite-wine/', views.FavoriteWineList.as_view()),
    path('api/customer/favorite-wine/<int:pk>/', views.FavoriteWineAddRemove.as_view()),
]