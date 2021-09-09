from django.urls import path
from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/admin/business', views.BusinessListRetrieveViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/business/<int:pk>/activate/', views.ActivateBusiness.as_view()),
    path('api/admin/business/<int:pk>/block/', views.BlockBusiness.as_view()),
]