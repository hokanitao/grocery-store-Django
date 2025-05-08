from django.urls import path
from . import views

# from django.contrib.auth import views as auth_views  # パスワードリセット用

urlpatterns = [
    path("login/", views.loginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    # For Customer-----
    path("mypage/", views.mypage, name="mypage"),
    path("history/", views.history, name="history"),
    path("buy/<int:pk>/", views.buy, name="buy"),
    path("productsList/", views.productsList, name="product_list"),
    path("added/", views.added, name="added"),
    # For Staff-----
    path("staffpage/", views.staffpage, name="staffpage"),
    path("basket/<int:pk>/", views.basketDetail, name="basketDetail"),
    path("basket/<int:pk>/confirm", views.confirm, name="confirm"),
    path("basket/<int:pk>/cancel", views.cancel, name="cancel"),
    path("userinfo/<int:pk>", views.userinfo, name="userinfo"),
]
