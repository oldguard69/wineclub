from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/admin/reward-program/', views.RewardProgramViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/winery/<int:pk>/reward-program/', views.RewardProgramOfAWinery.as_view())
]