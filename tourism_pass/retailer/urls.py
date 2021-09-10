from django.urls import path
from . import views
from base.constants import URL_MAPPING_FOR_VIEWSET_DETAIL, URL_MAPPING_FOR_VIEWSET_LIST

tourism_pass_list = views.TourismViewSet.as_view(URL_MAPPING_FOR_VIEWSET_LIST)
tourim_pass_detail = views.TourismViewSet.as_view(URL_MAPPING_FOR_VIEWSET_DETAIL)

urlpatterns = [
    path('api/business/<int:business_id>/tourism-pass/', tourism_pass_list),
    path('api/business/<int:business_id>/tourism-pass/<int:pk>/', tourim_pass_detail)
]