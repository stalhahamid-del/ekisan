from django.contrib import admin
from .models import Crops,Categories,Users,Profilepic,Subscription
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import User as AuthUser  # Import the Django user model for logging purposes

# Register your models here.

#admin.site.register(Crops)
#admin.site.register(Categories)
#admin.site.register(User)

# admin.site.register(Profilepic)




@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('categoryineng', 'categoryinhindi', 'categoryinurdu', 'color')
    search_fields = ('categoryineng',)
    list_per_page = 10

@admin.register(Crops)
class CropsAdmin(admin.ModelAdmin):
    list_display = ('category','nameineng', 'nameinhindi', 'nameinurdu')
    search_fields = ('category',)   
    list_per_page = 10

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'state', 'city', 'pincode', 'mobile', 'email' , 'role', 'created_at', 'updated_at', 'status')
    search_fields = ('name',)   
    list_per_page = 10    
    list_filter = ('state', 'city','role', 'status')

@admin.register(Profilepic)
class ProfilepicAdmin(admin.ModelAdmin):
    list_display = ('user', 'profilepic')
    search_fields = ('user',)           
    list_per_page = 10
    list_filter = ('user',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'planname', 'expiry_date', 'date', 'amount', 'razor_pay_order_id', 'razor_pay_payment_id', 'razor_pay_payment_signature' , 'paid')
    search_fields = ('user',)       
    list_per_page = 10

from django.contrib import messages

