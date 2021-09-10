from django.urls import path, include
from . import views

urlpatterns = [
    path('api/business/<int:business_id>/membership-program/', views.MembershipManagementView.as_view()),
    path('api/business/<int:business_id>/membership/joined/', views.MembershipJoinedCustomers.as_view()),
    path('api/business/<int:business_id>/membership/requested/', views.MembershipRequestCustomers.as_view()),
    path('api/business/<int:business_id>/membership/accept/', views.AcceptMembershipRequest.as_view()),
    path('api/business/<int:business_id>/membership/decline/', views.DeclineMembershipRequest.as_view()),
    path('api/business/<int:business_id>/membership/remove/', views.RemoveMembership.as_view())
]