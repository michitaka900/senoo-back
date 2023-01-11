from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.getProductData, name='products'),
    path('products/updatedb/', views.updateDB, name='update_db'),
]