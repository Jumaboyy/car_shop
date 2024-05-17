from django.urls import path
from .views import index, shop_detail, shop, login_view, product_by_category, cart, to_cart, register_view, clear_cart, log_out,detele_cart, create_checkout_sessions, success_payment

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:id>/', shop_detail, name='shop_detail'),
    path('shop/', shop, name='shop'),
    path('category/<int:category_id>/product', product_by_category, name='product_by_category'),
    path('cart/', cart, name='cart'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/',log_out, name='logout'),
    path('cart/', cart, name='cart'),
    path('to-cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('detele-cart/<int:id>/', detele_cart, name='detele_cart'),
    path('payment/', create_checkout_sessions, name='payment'),
    path('success/', success_payment, name='success'),
]
