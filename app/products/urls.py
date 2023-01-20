from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.getProductData, name='products'),
    path('products/ebay', views.getEbayItems, name='ebay'),
    path('products/ebay/item', views.getEbaySpecificItem, name='ebayItem'),
    path('products/ebay/token', views.getUserAccessToken, name='ebayToken'),
    path('products/updatedb/', views.updateDB, name='update_db'),

]