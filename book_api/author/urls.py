from rest_framework.routers import DefaultRouter
from author.views import AuthorViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)

urlpatterns = router.urls