from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced,Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

   
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'full_name',
        'city',
        'subcity',
        'specific_area',
        'mobile',
        'additional_phone',
    ]

    search_fields = [
        'full_name',
        'city',
        'mobile',
    ]

    list_filter = [
        'subcity',
        
    ]


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display= ['id', 'user', 'products', 'quantity']
    def products(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
@admin.register(Payment)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount','telebirr_order_id', 'telebirr_payment_status', 'telebirr_payment_id', 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'user_link', 'products', 'quantity', 'ordered_date', 'status', 'payments']

    def products(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    def user_link(self, obj):
        link = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', link, obj.user.username)

    def payments(self, obj):
        return "N/A"
    
    

@admin.register(Wishlist)
class wishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products']
    def products(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


    
    
admin.site.unregister(Group)