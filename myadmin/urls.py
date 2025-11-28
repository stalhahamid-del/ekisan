from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('logout/',views.logout,name="logout"),
    path('home/',views.home,name="home"),
    path('farmers/',views.farmer,name="farmer"),
    path('dealers/',views.dealer,name="dealer"),
    path('products/',views.products,name="products"),
    path('bits/',views.bits,name="bits"),

    path('categories/',views.categories,name="categories"),
    path('addcategory/',views.addcategory,name="addcategory"),
    path('editcategory/<int:id>/',views.editcategory,name="editcategory"),
    path('updatecategory/<int:id>/',views.updatecategory,name="updatecategory"),
    path('deletecategory/<int:id>/',views.deletecategory,name="deletecategory"),

    path('crops/',views.crops,name="crops"),
    path('addcrop/',views.addcrop,name="addcrop"),

    path('subscriptions/',views.subscriptions,name="subscription"),
    path('messages/',views.message,name="message"),
    path('farmerprofilepics/',views.farmerprofilepic,name="farmerprofilepic"),
    path('dealerprofilepics/',views.dealerprofilepic,name="dealerprofilepic"),
    path('dealerbitcount/',views.dealerbitcount,name="dealerbitcount"),

    path('check_new_farmer/',views.check_new_farmer,name="check_new_farmer"),
    path('check_new_dealer/',views.check_new_dealer,name="check_new_dealer"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)