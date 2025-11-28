from django.urls import path
from . import views
#from admin_notification.views import check_notification_view


app_name = 'farmer'

urlpatterns = [
    path('botpress_webhook_view/', views.botpress_webhook_view, name='botpress-webhook'),
    path('get_user_name/',views.get_user_name,name="get_user_name"),

    path('farmerprofile/',views.farmerprofile,name="farmerprofile"),
    path('editfarmerprofile/<int:id>/',views.editfarmerprofile,name="editfarmerprofile"),
    path('updatefarmerprofile/<int:id>/',views.updatefarmerprofile,name="updatefarmerprofile"),
    path('farmerprofilepic/',views.farmerprofilepic,name="farmerprofilepic"),
    path('changepassword/',views.changepassword,name="changepassword"),

    path('sales/',views.sales,name="sales"),
    path('crops/<int:id>/',views.crops,name="crops"),
    path('productprice/',views.productprice,name="productprice"),
    path('productpriceadd/',views.productpriceadd,name="productpriceadd"),
    path('productpriceadddone/<str:product_name>/<str:product_type>/<str:quality>/<int:rate>/<int:quantity>/',views.productpriceadddone,name="productpriceadddone"),

    path('farmerbit/',views.farmerbit,name="farmerbit"),
    path('bithistory/',views.bithistory,name="bithistory"),

    path('accept_bit/<int:dealerbit_id>/',views.accept_bit,name="accept_bit"),
    path('details/<str:bitter>/',views.details,name='details'),
    path('wait/<str:bitter>/',views.wait,name='wait'),

    path('subscription/',views.subscription,name="subscription"),
    path('freeplan/',views.freeplan,name="freeplan"),
    path('basicplan/<int:amount>',views.basicplan,name="basicplan"),
    path('standardplan/<int:amount>',views.standardplan,name="standardplan"),
    path('premiumplan/<int:amount>',views.premiumplan,name="premiumplan"),
    path('addbasicplan/<int:amount>',views.addbasicplan,name="addbasicplan"),

    path('success/<int:amount>/<str:payment_id>/<str:razorpay_payment_id>/<str:razorpay_order_id>/<str:razorpay_signature>/<str:plan>/',views.success,name="success"),

    path('farmerpayment_success/<str:id>/<str:payment_id>/<str:order_id>/<str:signature>/<int:amount>/<int:bit_id>/',views.farmerpayment_success,name="farmerpayment_success"),

    path('extendsubscription/',views.extendsubscription,name="extendsubscription"),

    path('farmeragreement/',views.farmeragreement,name="farmeragreement"),
    path('farmeragreementdone/',views.farmeragreementdone,name="farmeragreementdone"),
    
    path('getweather/',views.get_weather,name="get_weather"),
    
#    path('check/notification', check_notification_view, name="check_notifications"),

    path('paid/<int:amount>/<str:id>/<str:razorpay_payment_id>/<str:razorpay_order_id>/<str:razorpay_signature>/', views.paid, name='paid'),
]