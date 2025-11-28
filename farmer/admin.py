from django.contrib import admin
from .models import Product
# Register your models here.

#admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'product_type', 'quality', 'rate', 'quantity', 'created_at')
    search_fields = ('user',)   
    list_per_page = 10 