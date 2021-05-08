from django.contrib import admin
from django.urls import path, include
from datawork.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", homepage, name="home"),
    path("category/<str:slug>", cat_filter, name="category"),
    path("product/<int:item_id>", product_filter, name="product"),
    path("search", search, name="search"),
    path("cart", Cart, name="cart"),
    path("checkout", checkout, name="checkout"),
    path("myorder", myorder, name="myorder"),
    path("makepayment", makepayment, name="makepayment"),
    path("wishlist", Wishlist, name="wishlist"),
    path("add-to-cart/<int:item_id>/", addtocart, name="add-to-cart"),
    path("buynow/<int:item_id>", buynow, name="buynow"),
    path("remove-from-cart/<int:item_id>/", remove_cart, name="remove-from-cart"),
    path("cart-item-remove/<int:item_id>/", cart_item_remove, name="cart-item-remove"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

