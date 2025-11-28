from django.contrib import admin
from .models import Bit,DealerProfilepic,DealerBitCounts

# Register your models here.
#admin.site.register(Bit)
#admin.site.register(DealerProfilepic)


@admin.register(Bit)
class BitAdmin(admin.ModelAdmin):
    list_display = ('farmer_id', 'farmer', 'farmer_address', 'product', 'product_type', 'quality', 'rate', 'quantity', 'bit_value', 'bitter', 'bitter_address', 'status')
    search_fields = ('user',)    
    list_per_page = 5

@admin.register(DealerProfilepic)
class DealerProfilepicAdmin(admin.ModelAdmin):
    list_display = ('user', 'profilepic', )
    search_fields = ('user',)    
    list_per_page = 5

@admin.register(DealerBitCounts)
class DealerBitCountsAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan','current_bid_count' )
    search_fields = ('user',)    
    list_per_page = 5
