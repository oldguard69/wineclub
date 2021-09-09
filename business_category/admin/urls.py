from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/admin/business-categories', views.BusinessCategoryViewSet)

urlpatterns = router.urls