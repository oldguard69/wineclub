from .views import AuthorViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
urlpatterns = router.urls