from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('public/order', views.OrderViewSet),
router.register('public/create-order', views.CreateOrder)

urlpatterns = router.urls