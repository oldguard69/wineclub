from django.urls import path, include
from . import views

urlpatterns = [
    path('api/subscription-plans/', views.SubscriptionPlans.as_view()),
    path('api/create-subscription/', views.CreateSubscription.as_view()),
    path('api/cancel-subscription/', views.CancelSubscription.as_view())
]