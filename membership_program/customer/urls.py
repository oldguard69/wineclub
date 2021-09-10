from django.urls import path, include
from . import views

urlpatterns = [
    path('api/business/<int:business_id>/membership/ask-to-join/', views.RequestToJoinMembership.as_view()),
]