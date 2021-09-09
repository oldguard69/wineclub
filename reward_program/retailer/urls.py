from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/reward-program', views.RewardProgramViewSet)

urlpatterns = router.urls