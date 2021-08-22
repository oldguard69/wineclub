from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'publishers', views.PublisherViewSet)

urlpatterns = router.urls