from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/admin/membership', views.MembershipViewSet)

urlpatterns = router.urls