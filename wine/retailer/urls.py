from django.urls import path

from . import views
from base.constants import URL_MAPPING_FOR_VIEWSET_DETAIL, URL_MAPPING_FOR_VIEWSET_LIST

wine_list = views.WineViewSet.as_view(URL_MAPPING_FOR_VIEWSET_LIST)
wine_detail = views.WineViewSet.as_view(URL_MAPPING_FOR_VIEWSET_DETAIL)

urlpatterns = [
    path('api/business/<int:business_id>/wine/', wine_list, name="wine-list"),
    path('api/business/<int:business_id>/wine/<int:pk>/', wine_detail, name='wine-detail'),
]