from django.shortcuts import redirect,render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from accounts.models import Users, Subscription
from farmer.models import Paid
from dealer.models import Bit,DealerProfilepic
from datetime import date
import razorpay

class AuthMiddlewareDealer(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id is None and request.path.startswith('/dealer/'):
            return redirect('/index/')
        if user_id:
            try:
                user = Users.objects.get(id=user_id)
                role = user.role
                if role == 'Dealer' and 'farmer' in request.path or request.path.startswith('/admin/'):
                    return redirect('/dealer/dealersprofile/')
                if user_id and request.path == '/index/' or request.path == '/register/' or request.path == '/forget/' or request.path == '/' or request.path == '/termsandconditions/' or request.path == 'privacypolicy' or request.path == '/password/':
                    return redirect('/dealer/dealersprofile/')
                
            except Users.DoesNotExist:
                pass
        return None
    


class SubscriptionMiddlewareDealer(MiddlewareMixin):
    def process_request(self,request):
        today = date.today()
        expired_subscriptions = Subscription.objects.filter(expiry_date__lt=today)
        if expired_subscriptions:
            expired_subscriptions.delete()
        else:
            return None


class PaymentnMiddlewareDealer(MiddlewareMixin):
    def process_request(self,request):
        try:
            user_id=request.session.get('user_id')
            user=Users.objects.get(id=user_id)
            role=user.role
            user_name=user.name
            profilepic=DealerProfilepic.objects.get(user=user)
            paid=Paid.objects.filter(user=user)
            bits=Bit.objects.filter(bitter=user_name,status='True')
            for bit in bits:
                rate=bit.bit_value
                quantity=bit.quantity.split()
                amount= (float(rate) * float(quantity[0]) * 2) / 100
                client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
                payment = client.order.create({'amount': int(float(amount) * 100), 'currency': "INR", 'payment_capture': '1'})
            if user_id and not paid.exists() and role=="Dealer" and not request.path.startswith('/dealer/pay/') and not request.path.startswith('/dealer/payment_success/') and not request.path.startswith('/media/profile_pics/'):
                return render(request,'payments_dealer.html',{'payment':payment,'user_name':user_name,'profilepic':profilepic,'bits':bits})
        except:
            pass        
        return None
