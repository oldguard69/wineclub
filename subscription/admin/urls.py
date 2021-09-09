from django.urls import path, include

from . import views
urlpatterns = [
    path('api/subscriptions/', views.SubscriptionListCreate.as_view()),
    path('api/subscriptions/<int:pk>/', views.SubscriptionRetrieveUpdate.as_view())
]