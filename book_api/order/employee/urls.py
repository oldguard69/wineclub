from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('orders', views.OrderVS)

urlpatterns = [
    path('', include(router.urls)),
    path('accept-order', views.AcceptOrder.as_view()),
    path('cancel-order', views.CancelOrder.as_view())

]
