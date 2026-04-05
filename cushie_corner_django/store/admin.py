from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem, ContactMessage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    list_editable = ['price', 'stock']
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'total', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_editable = ['is_read']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'product', 'quantity', 'added_at']
