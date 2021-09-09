from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/tourism-pass', views.TourismViewSet)

urlpatterns = router.urls