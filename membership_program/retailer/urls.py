from django.urls import path, include
from . import views

urlpatterns = [
    path('api/business/<int:business_id>/membership/', views.MembershipManagementView.as_view())
]