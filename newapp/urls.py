from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User Dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<uuid:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<uuid:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order/<uuid:order_id>/', views.order_detail, name='order_detail'),
    
    # Prescriptions
    path('prescriptions/', views.my_prescriptions, name='my_prescriptions'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
    
    # Contact & Info
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
