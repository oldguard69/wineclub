from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/business', views.BusinessViewSet)

urlpatterns = router.urls