from django.urls import path
from . import views
from base.constants import URL_MAPPING_FOR_VIEWSET_DETAIL, URL_MAPPING_FOR_VIEWSET_LIST

reward_program_list = views.RewardProgramViewSet.as_view(URL_MAPPING_FOR_VIEWSET_LIST)
reward_program_detail = views.RewardProgramViewSet.as_view(URL_MAPPING_FOR_VIEWSET_DETAIL)

urlpatterns = [
    path('api/business/<int:business_id>/reward-program/', reward_program_list),
    path('api/business/<int:business_id>/reward-program/<int:pk>/', reward_program_detail),
]