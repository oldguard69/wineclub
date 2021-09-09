from django.urls import path, include
from . import views

urlpatterns = [
    path('api/membership/', views.MembershipView.as_view())
]