from django.urls import include, path
from cart import views

urlpatterns = [
    path(r'cart/', views.CartView.as_view()),
    path(r'cart/<int:pk>', views.DeleteCartItem.as_view()),
    path(r'merge-cart/', views.MergeCart.as_view())
]