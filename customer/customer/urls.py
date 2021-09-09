from django.urls import path
from . import views

urlpatterns = [
    path('api/profile/customer/', views.CustomerProfile.as_view()),
    path('api/profile/customer/favorite-region/', views.UpdateFavoriteRegion.as_view()),
    path('api/profile/customer/favorite-wine-type/', views.UpdateFavoriteWineType.as_view())
]