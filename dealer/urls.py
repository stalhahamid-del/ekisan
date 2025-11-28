from django.contrib import admin
from django.urls import path
from . import views
#from admin_notification.views import check_notification_view


urlpatterns = [
    path('addbuy/',views.addbuy,name="addbuy"),  
    path('buy/',views.buy,name="buy"),
    path('crops/<int:id>/',views.crops,name="crops"),
    
    
    path('dealersprofile/',views.dealersprofile,name="dealersprofile"),
    path('editdealerprofile/<int:id>/',views.editdealerprofile,name="editdealerprofile"),
    path('updatedealerprofile/<int:id>/',views.updatedealerprofile,name="updatedealerprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('dealerprofilepic/',views.dealerprofilepic,name="dealerprofilepic"),

    path('productcategory/',views.productcategory,name="productcategory"),
    path('productcategorylist/',views.productcategorylist,name="productcategorylist"), 

    path('productlist/<str:fruit>/',views.productlist,name="productlist"),
    
    path('bit/<int:user_id>/<str:user_name>/<str:product_name>/<str:product_type>/<str:quality>/<str:rate>/<str:quantity>/',views.bit,name="bit"),
    path('process_bit/<int:user_id>/<str:user_name>/<str:product_name>/<str:product_type>/<str:quality>/<str:rate>/<str:quantity>/', views.process_bit, name='process_bit'),

    path('mybits/', views.mybits, name='mybits'),

    path('get_notifications/', views.get_notifications, name='get_notifications'),

    path('subscription/',views.subscription,name="subscription"),
    path('freeplan/',views.freeplan,name="freeplan"),
    path('basicplan/<int:amount>',views.basicplan,name="basicplan"),
    path('standardplan/<int:amount>',views.standardplan,name="standardplan"),
    path('premiumplan/<int:amount>',views.premiumplan,name="premiumplan"),

    path('success/<int:amount>/<str:payment_id>/<str:razorpay_payment_id>/<str:razorpay_order_id>/<str:razorpay_signature>/<str:plan>/',views.success,name="success"),
    
    path('pay/<int:amount>/<str:name>/<str:quantity>/',views.pay,name="pay"),

    path('payment_success/<str:id>/<str:payment_id>/<str:order_id>/<str:signature>/<int:amount>/<int:bit_id>/',views.payment_success,name="payment_success"),

    path('extendsubscription/',views.extendsubscription,name="extendsubscription"),

#    path('check/notification', check_notification_view, name="check_notifications"),
]