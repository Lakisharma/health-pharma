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
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
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
    path('order/<uuid:order_id>/invoice/', views.order_invoice, name='order_invoice'),
    
    # Prescriptions
    path('prescriptions/', views.my_prescriptions, name='my_prescriptions'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
    
    # Contact & Info
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    # Admin Panel
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Categories
    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('admin-category/add/', views.admin_category_add, name='admin_category_add'),
    path('admin-category/edit/<int:category_id>/', views.admin_category_edit, name='admin_category_edit'),
    path('admin-category/delete/<int:category_id>/', views.admin_category_delete, name='admin_category_delete'),
    
    # Products
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-product/add/', views.admin_product_add, name='admin_product_add'),
    path('admin-product/edit/<uuid:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-product/delete/<uuid:product_id>/', views.admin_product_delete, name='admin_product_delete'),
    
    # Orders
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order/<uuid:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-order/edit/<uuid:order_id>/', views.admin_order_edit, name='admin_order_edit'),
    path('admin-order/delete/<uuid:order_id>/', views.admin_order_delete, name='admin_order_delete'),
    
    # Prescriptions
    path('admin-prescriptions/', views.admin_prescriptions, name='admin_prescriptions'),
    path('admin-prescription/<uuid:prescription_id>/', views.admin_prescription_detail, name='admin_prescription_detail'),
    path('admin-approve-prescription/<uuid:prescription_id>/', views.admin_approve_prescription, name='admin_approve_prescription'),
    
    # Users
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-user/edit/<int:user_id>/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-user/toggle-status/<int:user_id>/', views.admin_user_toggle_status, name='admin_user_toggle_status'),
    
    # Reviews
    path('admin-reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin-review/delete/<int:review_id>/', views.admin_review_delete, name='admin_review_delete'),
    
    # Messages
    path('admin-messages/', views.admin_messages, name='admin_messages'),
    path('admin-message/delete/<int:message_id>/', views.admin_message_delete, name='admin_message_delete'),
    
    # Company Settings
    path('admin-company-settings/', views.admin_company_settings, name='admin_company_settings'),
    
    # Notifications
    path('admin-notifications/mark-read/', views.admin_mark_notifications_read, name='admin_mark_notifications_read'),
]
