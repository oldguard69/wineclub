from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/business-categories', views.BusinessCategoryViewSet)

urlpatterns = router.urls