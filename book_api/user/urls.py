from django.urls import path


from user import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('register/', views.Register.as_view()),
    path('request-update-email/', views.RequestUpdateEmail.as_view()),
    path('verify-update-email/', views.VerifyUpdateEmail.as_view()),
    path('profile/', views.UserProfile.as_view())
]