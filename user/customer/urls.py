from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.Register.as_view()),
]