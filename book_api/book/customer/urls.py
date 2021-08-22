from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('public/books', views.BookViewSet)

urlpatterns = router.urls