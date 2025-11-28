from django.shortcuts import redirect,render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from accounts.models import Users, Subscription,Profilepic
from farmer.models import Paid,Bit
from dealer.models import DealerBitCounts
from datetime import date
import razorpay

class AuthMiddlewareFarmer(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id is None and request.path.startswith('/farmer/'):
            return redirect('/index/')
        if user_id:
            try:
                user = Users.objects.get(id=user_id)
                role = user.role
                if role == 'Farmer' and 'dealer' in request.path or request.path.startswith('/admin/'):
                    return redirect('/farmer/farmerprofile/')
                if user_id and request.path == '/index/' or request.path == '/register/' or request.path == '/forget/' or request.path == '/' or request.path == '/termsandconditions/' or request.path == 'privacypolicy' or request.path == '/password/':
                    return redirect('/farmer/farmerprofile/')
            except Users.DoesNotExist:
                pass
        return None

class SubscriptionMiddlewareFarmer(MiddlewareMixin):
    def process_request(self,request):
        today = date.today()
        expired_subscriptions = Subscription.objects.filter(expiry_date__lt=today)
        print('expired_subscriptions',expired_subscriptions)
        if expired_subscriptions.exists():
            expired_subscriptions.delete()
            dealerbitcount = DealerBitCounts.objects.filter(subscription_plan__in=expired_subscriptions)
            dealerbitcount.delete()
        else:
            return None
        
    

class PaymentnMiddlewareFarmer(MiddlewareMixin):
    def process_request(self,request):
        print('farmermiddlewarepayment')
        try:
            user_id=request.session.get('user_id')
            user=Users.objects.get(id=user_id)
            role=user.role
            user_name=user.name
            profilepic=Profilepic.objects.get(user=user)
            paid=Paid.objects.filter(user=user)
            print(paid)
            bits=Bit.objects.filter(farmer_id=user,status='True')
            print(bits)
            for bit in bits:
                dealername=bit.bitter
            print(dealername)
            dealers=Users.objects.filter(name=dealername)
            print(dealers)
            for dealer in dealers:
                dealerpaid=Paid.objects.filter(user=dealer,paid=True)
            print(dealerpaid)
            dealerpaid_bits = []
            for bit in bits:
                dealer_payment = Paid.objects.filter(paidfor=bit, paid=True)
                if dealer_payment.exists():
                    dealerpaid_bits.append(bit.id)
                rate=bit.bit_value
                quantity=bit.quantity.split()
                amount= (float(rate) * float(quantity[0]) ) / 100
                client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
                payment = client.order.create({'amount': int(float(amount) * 100), 'currency': "INR", 'payment_capture': '1'})
                    
            print('dealerpaid_bits',dealerpaid_bits)
            if user_id and not paid.exists() and role=="Farmer" and dealerpaid and not request.path.startswith('/farmer/farmerpayment_success/') and not request.path.startswith('/farmer/details/') and not request.path.startswith('/media/profile_pics/'):
                return render(request,'payments_farmer.html',{'user_name':user_name,'payment':payment,'dealerpaid_bits':dealerpaid_bits,'profilepic':profilepic,'bits':bits})
        except:
            pass        
        return None


