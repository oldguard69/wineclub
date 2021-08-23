from django.urls import path, include


from user import views

urlpatterns = [
    path('', include('user.customer.urls')),
    path('login/', views.Login.as_view()),
    path('request-update-email/', views.RequestUpdateEmail.as_view()),
    path('verify-update-email/', views.VerifyUpdateEmail.as_view()),
    path('profile/', views.UserProfile.as_view())
]