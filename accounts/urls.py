from django.urls import path
from . import views
#from admin_notification.views import check_notification_view

urlpatterns = [
    path('',views.home,name="home"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('privacypolicy/',views.privacypolicy,name="privacypolicy"),
    path('termsandconditons/',views.termsandconditons,name="termsandconditons"),
    
    path('otp/',views.otp,name="otp"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    
    path('index/',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('forget/',views.forget,name="forget"),
    path('logout/', views.logout, name='logout'),
    
#    path('check/notification', check_notification_view, name="check_notifications"),
    
]

