from django.urls import path
from apps.product.views.admin_views import Director
from apps.product.views.shop_views import Shop

urlpatterns = [
    path("", Director.as_view(), name="dashboard"),
    path("shop/", Shop.as_view(), name="shop")
]
