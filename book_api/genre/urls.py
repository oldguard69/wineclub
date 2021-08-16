from django.urls import path
from genre.views import GenreViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres', GenreViewSet)

urlpatterns = router.urls