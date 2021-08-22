from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('genres', views.GenreViewSet)

urlpatterns = router.urls