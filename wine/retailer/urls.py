from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/wine', views.WineViewSet)

urlpatterns = router.urls