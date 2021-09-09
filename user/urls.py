from django.urls import path, include

from user import views

urlpatterns = [
    path('api/login/', views.Login.as_view()),
    path('api/change-password/', views.ChangePassword.as_view()),
    path('api/forgot-password/', views.ForgotPassword.as_view()),
    path('api/reset-password/', views.ResetPassword.as_view()),
    path('', include('user.customer.urls')),
]