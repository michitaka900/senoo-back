from django.urls import path
from . import views

urlpatterns = [
    path('products', views.getProductData, name='products'),
    path('products/shopify', views.findShopifyItems, name='shopify'),
    path('products/ebay', views.getEbayItems, name='ebay'),
    path('products/ebay/item', views.getEbaySpecificItem, name='ebay-items'),
    path('products/create', views.createShopifyProduct, name='create_product'),
    path('products/update', views.updateInventory, name='update_product'),
    path('products/ebay/inventory', views.checkInventory, name='check-inventory'),
    path('products/ebay/token', views.getUserAccessToken, name='ebayToken'),
    path('currency/rates', views.get_exchange_rate, name='currency-rate'),
    path('products/ebay/seller', views.getSellerItems, name='seller-items'),
    path('user/login/', views.login_user, name='user-login'),
]