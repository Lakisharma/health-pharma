from django.contrib import admin
from .models import (
    CompanyInfo, Category, Product, Review, Prescription, Cart, CartItem,
    Order, OrderItem, ContactMessage, Notification
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone', 'email', 'city']
    fieldsets = (
        ('Company Details', {'fields': ('company_name', 'phone', 'email')}),
        ('Address', {'fields': ('address', 'city', 'state', 'zip_code')}),
        ('Additional Info', {'fields': ('about', 'logo')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'rating', 'is_active']
    list_filter = ['is_active', 'category', 'requires_prescription', 'created_at']
    search_fields = ['name', 'generic_name', 'manufacturer']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'generic_name', 'category', 'description')}),
        ('Pricing', {'fields': ('price', 'discount_price')}),
        ('Specifications', {'fields': ('unit', 'strength', 'manufacturer', 'expiry_date')}),
        ('Inventory', {'fields': ('stock',)}),
        ('Additional', {'fields': ('requires_prescription', 'rating', 'is_active', 'image')}),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username']
    readonly_fields = ['created_at']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor_name', 'prescription_date', 'verified', 'uploaded_at']
    list_filter = ['verified', 'uploaded_at']
    search_fields = ['user__username', 'doctor_name']
    fieldsets = (
        ('Prescription Details', {'fields': ('user', 'doctor_name', 'prescription_date', 'file')}),
        ('Verification', {'fields': ('verified', 'notes')}),
    )
    readonly_fields = ['uploaded_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_item_count', 'get_total', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_total']
    search_fields = ['product__name', 'cart__user__username']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total']
    fields = ['product', 'quantity', 'price', 'get_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'shipping_email']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'total_amount', 'status')}),
        ('Payment', {'fields': ('payment_method', 'payment_status')}),
        ('Shipping Address', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_email', 'shipping_address', 
                      'shipping_city', 'shipping_state', 'shipping_zip')
        }),
        ('Prescription', {'fields': ('prescription_required', 'prescription')}),
        ('Notes', {'fields': ('notes',)}),
    )
    readonly_fields = ['order_number', 'created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total']
    search_fields = ['order__order_number', 'product__name']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at', 'name', 'email', 'phone', 'subject', 'message']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_read', 'order', 'created_at']
    list_filter = ['is_read', 'is_admin', 'created_at']
    search_fields = ['title', 'message', 'order__order_number']
    readonly_fields = ['created_at']
