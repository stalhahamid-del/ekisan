from django.shortcuts import render,redirect
from accounts.models import Users,Subscription,Profilepic,Categories,Crops,Free
from farmer.models import Product,Agreement,Paid
from dealer.models import Bit
from django.urls import reverse 
from django.http import JsonResponse,HttpResponse
import razorpay
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import os
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from collections import defaultdict
from django.conf import settings
from twilio.rest import Client
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


def get_user_name(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        user_name = user.name
    return JsonResponse({'user_name': user_name})



@csrf_exempt
def botpress_webhook_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input', '')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        if not user_input:
            return JsonResponse({'error': 'No user input provided'}, status=400)
        bot_response = handle_user_command(user_input)
        print(bot_response)
        return JsonResponse(bot_response)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def handle_user_command(user_input):
        user_input = user_input.lower()
        command_to_route = {
        'ओपन प्रोफाइल': '/farmer/farmerprofile/',
        'ओपन सेल्स': '/farmer/sales/',
        'ओपन डेट्स ऑन माय प्रोडक्ट्स': '/farmer/farmerbit/',
        'ओपन माय प्रोडक्ट्स': '/farmer/productprice/',
        'ओपन माय बीट हिस्ट्री': '/farmer/bithistory/',
        'ओपन वेदर': '/farmer/getweather/',
        # Add more commands and routes as needed
        }
        default_response = {'message': 'अज्ञात कमांड। कृपया पुनः प्रयास करें।'}
        if user_input in command_to_route:
                return {'message': f'{user_input.replace("ओपन ", "").capitalize()}', 'url': command_to_route[user_input]}
        else:
                return default_response    





def farmerprofile(request):
        try:
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                        print('username',user_name)
                profile = Users.objects.get(id=user_id)
                profilepic = None
                subscription=Subscription.objects.filter(user=profile) 
                print('hey',subscription)
                profilepic=Profilepic.objects.get(user=profile)       
                print('hi',profilepic)
                return render(request, 'farmerprofile_farmer.html', {'profile': profile,'profilepic':profilepic,'user_name':user_name,'subscription':subscription})
        except Subscription.DoesNotExist:
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                        print('username',user_name)
                profile = Users.objects.get(id=user_id)
                profilepic = None
                profilepic=Profilepic.objects.get(user=profile)
                return render(request, 'farmerprofile_farmer.html', {'profile': profile,'profilepic':profilepic,'user_name':user_name,'subscription':subscription})
        except Profilepic.DoesNotExist:
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                        print('username',user_name)
                profile = Users.objects.get(id=user_id)
                profilepic = None
                subscription=Subscription.objects.filter(user=profile)
                return render(request, 'farmerprofile_farmer.html', {'profile': profile,'profilepic':profilepic,'user_name':user_name,'subscription':subscription})
        

def editfarmerprofile(request,id):
    try:   
       farmer=Users.objects.get(id=id)
       user_id = request.session.get('user_id')
       if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
       profilepic=Profilepic.objects.get(user=user) 
       return render(request,'editfarmerprofile_farmer.html',{'farmer':farmer,'profilepic':profilepic,'user_name':user_name})       
    except:
       farmer=Users.objects.get(id=id)
       user_id = request.session.get('user_id')
       if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
       return render(request,'editfarmerprofile_farmer.html',{'farmer':farmer,'user_name':user_name})       


def updatefarmerprofile(request,id):
       user=Users.objects.get(id=id)
       if request.method=='POST':
              user.name=request.POST['name']
              user.address=request.POST['address']
              user.city=request.POST['city']
              user.state=request.POST['state']
              user.save()
              return redirect('/farmer/farmerprofile/') 
       return redirect(f'/farmer/editfarmerprofile/{id}/') 


def farmerprofilepic(request):
    if request.method == 'POST' and request.FILES.get('profilepic'):
        user_id = request.session.get('user_id')
        user = Users.objects.get(id=user_id)  # Assuming the user is authenticated
        profile, created = Profilepic.objects.get_or_create(user=user)
        
        profile.profilepic = request.FILES['profilepic']
        profile.save()
        
        return redirect('/farmer/farmerprofile/')
    return redirect('/farmer/farmerprofile/')



def changepassword(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = Users.objects.get(id=user_id)
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_password')
        
        encrypted_password = user.password
        encrypted_password = encrypted_password[2:len(encrypted_password)-1]
        key = settings.FERNET_KEY
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        print('decrypted_password',decrypted_password)

        if new_password == confirm_new_password:
             if current_password == decrypted_password:
                encrypted_new_password = new_password
                key = settings.FERNET_KEY
                cipher_suite = Fernet(key)
                encrypted_new_password = cipher_suite.encrypt(encrypted_new_password.encode())
                user.password = encrypted_new_password
                user.save()
                print('password changed')
                return redirect('/farmer/farmerprofile/')
             else:
                messages = 'New password and confirm password do not match.'
        else:
            try:
                messages = 'Current password is incorrect.'
                profilepic=Profilepic.objects.get(user=user) 
                subscription=Subscription.objects.get(user=user)
                return render(request, 'farmerprofile_farmer.html', {'profile': user,'profilepic':profilepic,'subscription':subscription,'error_messages': messages})
            except:
                messages = 'Current password is incorrect.'
                user_id = request.session.get('user_id')
                user = Users.objects.get(id=user_id)
                user_name=user.name
                return render(request, 'farmerprofile_farmer.html', {'profile': user,'user_name':user_name,'error_messages': messages})              
    return render(request, 'farmerprofile_farmer.html')




def productprice(request):
    try:
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name   
        user=Users.objects.get(id=user_id)    
        products=Product.objects.filter(user=user)  
        profilepic=Profilepic.objects.get(user=user)   
        return render(request, 'Productsprice_farmer.html', {'products': products,'profilepic':profilepic,'user_name':user_name})
    except:
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name   
        user=Users.objects.get(id=user_id)    
        products=Product.objects.filter(user=user)  
        return render(request, 'Productsprice_farmer.html', {'products': products,'user_name':user_name})
           


def productpriceadd(request):
    try:
        user_id = request.session.get('user_id')
        fruit_name = request.GET.get('fruit', '')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
                user_subscription = Subscription.objects.filter(user=user, planname='free').first()
                if user_subscription:
                        has_added_product = Product.objects.filter(user=user).exists()                
                        current_date = datetime.now().date()
                        expiry_date = user_subscription.date + timedelta(days=3)
                       
                basic_subscription = Subscription.objects.filter(user=user, planname='basic').first()
                if basic_subscription:
                        current_date = datetime.now().date()
                        expiry_date = basic_subscription.date + timedelta(days=30)  
                        product_count = Product.objects.filter(user=user).count()

                standard_subscription = Subscription.objects.filter(user=user, planname='standard').first()
                if standard_subscription:
                        current_date = datetime.now().date()
                        expiry_date = standard_subscription.date + timedelta(days=30)  # Assuming 1 month validity
                        product_count = Product.objects.filter(user=user).count()
                
                premium_subscription = Subscription.objects.filter(user=user, planname='premium').first()
                if premium_subscription: 
                        current_date = datetime.now().date()
                        expiry_date = premium_subscription.date + timedelta(days=30)  # Assuming 1 month validity

                if user_id:
                        user = Users.objects.get(id=user_id)
                        products = Product.objects.filter(user=user)
                        profilepic=Profilepic.objects.get(user=user) 
                        return render(request, 'Productspriceadd_farmer.html', {'fruit_name': fruit_name,'profilepic':profilepic,'products': products, 'user_name': user_name})
                
    except:
        user_id = request.session.get('user_id')
        fruit_name = request.GET.get('fruit', '')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
                user_subscription = Subscription.objects.filter(user=user, planname='free').first()
                if user_subscription:
                        has_added_product = Product.objects.filter(user=user).exists()                
                        current_date = datetime.now().date()
                        expiry_date = user_subscription.date + timedelta(days=3)
                        
                basic_subscription = Subscription.objects.filter(user=user, planname='basic').first()
                if basic_subscription:
                        current_date = datetime.now().date()
                        expiry_date = basic_subscription.date + timedelta(days=30)  # Assuming 1 month validity
                        product_count = Product.objects.filter(user=user).count()
                
                standard_subscription = Subscription.objects.filter(user=user, planname='standard').first()
                if standard_subscription:
                        current_date = datetime.now().date()
                        expiry_date = standard_subscription.date + timedelta(days=30)  # Assuming 1 month validity
                        product_count = Product.objects.filter(user=user).count()
                
                premium_subscription = Subscription.objects.filter(user=user, planname='premium').first()
                if premium_subscription:
                        current_date = datetime.now().date()
                        expiry_date = premium_subscription.date + timedelta(days=30)  # Assuming 1 month validity

                if user_id:
                        user = Users.objects.get(id=user_id)
                        products = Product.objects.filter(user=user)
                        return render(request, 'Productspriceadd_farmer.html', {'fruit_name': fruit_name,'products': products, 'user_name': user_name})
               





from datetime import datetime, timedelta

def productpriceadddone(request, product_name, product_type, quality, rate, quantity):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/index/')  # Redirect to login if user is not logged in

        fruit_name = request.GET.get('fruit', '')

        try:
            user = Users.objects.get(pk=user_id)
            user_name = user.name
        except Users.DoesNotExist:
            return render(request, 'cantaddProducts_farmer.html', {'error': 'User not found.'})

        try:
            profilepic = Profilepic.objects.get(user=user)
        except Profilepic.DoesNotExist:
            profilepic = None  # Handle the case where a user might not have a profile picture

        # Initialize variables
        max_products_allowed = 0
        current_date = datetime.now().date()

        try:
            # Get all active subscriptions and calculate total permissions
            user_subscriptions = Subscription.objects.filter(user=user, paid=True, expiry_date__gte=current_date)
        except Subscription.DoesNotExist:
            user_subscriptions = []  # Handle case where no subscriptions are found

        for subscription in user_subscriptions:
            if subscription.planname == 'free':
                max_products_allowed += 1
            elif subscription.planname == 'basic':
                max_products_allowed += 4
            elif subscription.planname == 'standard':
                max_products_allowed += 10
            elif subscription.planname == 'premium':
                max_products_allowed = float('inf')  # Unlimited products
                break  # No need to check further if premium subscription is found

        # Check if the user has already added the maximum number of products
        product_count = Product.objects.filter(user=user).count()
        if product_count >= max_products_allowed:
            return render(request, 'cantaddProducts_farmer.html', {
                'fruit_name': fruit_name,
                'profilepic': profilepic,
                'user_name': user_name,
                'error': f'You can add up to {max_products_allowed} products based on your subscriptions.'
            })

        # Handle the product addition
        if request.method == 'POST':
            try:
                Product.objects.create(
                    user=user,
                    product_name=product_name,
                    product_type=product_type,
                    quality=quality,
                    rate=rate,
                    quantity=quantity
                )
            except Exception as e:
                return render(request, 'error_template.html', {'error_message': f'Error adding product: {str(e)}'})

            products = Product.objects.filter(user=user)
            return render(request, 'Productsprice_farmer.html', {
                'products': products,
                'profilepic': profilepic,
                'user_name': user_name
            })

        products = Product.objects.filter(user=user)
        return render(request, 'Productspriceadd_farmer.html', {
            'fruit_name': fruit_name,
            'profilepic': profilepic,
            'products': products,
            'user_name': user_name
        })

    except Exception as e:
        print(f"Error: {e}")
        # Handle any other errors or exceptions here
        return render(request, 'cantaddProducts_farmer.html', {'error': str(e)})





def sales(request):
        try:
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                categories=Categories.objects.all()
                profilepic=Profilepic.objects.get(user=user)
                return render(request,'sales_farmer.html',{'user_name':user_name,'categories':categories,'profilepic':profilepic})
        except:                         
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                categories=Categories.objects.all()
                return render(request,'sales_farmer.html',{'user_name':user_name,'categories':categories})

def crops(request, id):
    try:
        user_id = request.session.get('user_id')
        user_name = ""
        if user_id:
            user = Users.objects.get(pk=user_id)
            user_name = user.name
        
        crops = Crops.objects.filter(category=id)
        fruit = Categories.objects.get(id=id)
        profilepic = Profilepic.objects.get(user=user) 
        
        crops_with_farmers = []
        for crop in crops:
            name = crop.nameineng
            accepted_bits = Bit.objects.filter(product=name, status=True)
    
            # Set farmer_count to 0 if there are accepted bits, otherwise count the products
            if accepted_bits.exists():
                farmer_count = 0
            else:
                farmer_count = Product.objects.filter(product_name=name).count()
                
            crops_with_farmers.append({
                'crop': crop,
                'farmer_count': farmer_count
            })
        
        # Sort the list of dictionaries by 'farmer_count'
        crops_with_farmers = sorted(crops_with_farmers, key=lambda x: x['farmer_count'], reverse=True)
        
        return render(request, 'subcategories_farmer.html', {
            'user_name': user_name,
            'fruit': fruit,
            'profilepic': profilepic,
            'crops_with_farmers': crops_with_farmers
        })
        
    except Exception as e:
        # Optionally log the exception or handle it as needed
        print(f"An error occurred: {e}")
        
        # Repeat the same logic as above but without the profilepic (if that is the cause of the error)
        user_id = request.session.get('user_id')
        user_name = ""
        if user_id:
            user = Users.objects.get(pk=user_id)
            user_name = user.name
        
        crops = Crops.objects.filter(category=id)
        fruit = Categories.objects.get(id=id)
        
        crops_with_farmers = []
        for crop in crops:
            name = crop.nameineng
            accepted_bits = Bit.objects.filter(product=name, status=True)
    
            # Set farmer_count to 0 if there are accepted bits, otherwise count the products
            if accepted_bits.exists():
                farmer_count = 0
            else:
                farmer_count = Product.objects.filter(product_name=name).count()
                
            crops_with_farmers.append({
                'crop': crop,
                'farmer_count': farmer_count
            })
        
        # Sort the list of dictionaries by 'farmer_count'
        crops_with_farmers = sorted(crops_with_farmers, key=lambda x: x['farmer_count'], reverse=True)
        
        return render(request, 'subcategories_farmer.html', {
            'user_name': user_name,
            'fruit': fruit,
            'crops_with_farmers': crops_with_farmers
        })



def farmerbit(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
            bit_data = Bit.objects.filter(farmer_id=user).values(
                'id', 'product', 'bitter', 'product_type', 'quantity', 
                'rate', 'quality', 'bit_value', 'status'
            )
            
            # Filter out bits with status True
            filtered_bit_data = [bit for bit in bit_data if bit['status'] != 'True']
            profilepic=Profilepic.objects.get(user=user) 
            # Organize filtered_bit_data by product
            bit = {}
            for entry in filtered_bit_data:
                product_name = entry['product']
                if product_name not in bit:
                    bit[product_name] = []
                bit[product_name].append(entry)
            
            context = {
                'bit': bit,
                'profilepic':profilepic,
                'user_name': user.name
            }
            return render(request, 'farmerbit_farmer.html', context)
        
        except:
            user_id = request.session.get('user_id')
            if user_id:
                
                user = Users.objects.get(id=user_id)
                bit_data = Bit.objects.filter(farmer_id=user).values(
                        'id', 'product', 'bitter', 'product_type', 'quantity', 
                        'rate', 'quality', 'bit_value', 'status'
                )
                
                # Filter out bits with status True
                filtered_bit_data = [bit for bit in bit_data if bit['status'] != 'True'] 
                # Organize filtered_bit_data by product
                bit = {}
                for entry in filtered_bit_data:
                        product_name = entry['product']
                        if product_name not in bit:
                                bit[product_name] = []
                                bit[product_name].append(entry)
                
                context = {
                        'bit': bit,
                        'user_name': user.name
                }
                return render(request, 'farmerbit_farmer.html', context)
    else:
        return render(request, 'error.html', {'message': 'User ID not found in session'})




def bithistory(request):
    try:
        id=request.session.get('user_id')
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        user=Users.objects.get(id=id)
        bits = Bit.objects.filter(farmer_id=user)
        bits_by_year = defaultdict(lambda: defaultdict(lambda: {'accepted': [], 'rejected': []}))
        for bit in bits:
                year = bit.created_at.year
                if bit.status == 'True':
                        bits_by_year[year][bit.product]['accepted'].append(bit)
                elif bit.status == 'Rejected':
                        bits_by_year[year][bit.product]['rejected'].append(bit)

        bits_by_year = {year: dict(products) for year, products in bits_by_year.items()}
        bits_by_year = {year: {product: dict(status) for product, status in products.items()} for year, products in bits_by_year.items()}
        profilepic=Profilepic.objects.get(user=user) 
        return render(request,'bithistory_farmer.html',{'bits_by_year': bits_by_year,'user_name':user_name,'profilepic':profilepic} )
    except:
        id=request.session.get('user_id')
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        user=Users.objects.get(id=id)
        bits = Bit.objects.filter(farmer_id=user)
        bits_by_year = defaultdict(lambda: defaultdict(lambda: {'accepted': [], 'rejected': []}))
        for bit in bits:
                year = bit.created_at.year
                if bit.status == 'True':
                        bits_by_year[year][bit.product]['accepted'].append(bit)
                elif bit.status == 'Rejected':
                        bits_by_year[year][bit.product]['rejected'].append(bit)

        bits_by_year = {year: dict(products) for year, products in bits_by_year.items()}
        bits_by_year = {year: {product: dict(status) for product, status in products.items()} for year, products in bits_by_year.items()}
        return render(request,'bithistory_farmer.html',{'bits_by_year': bits_by_year,'user_name':user_name} )

        

def accept_bit(request, dealerbit_id):
    if request.method == 'POST':
        try:
                dealer_bit = Bit.objects.get(pk=dealerbit_id)
                farmer_bit = dealer_bit.status
                product_bit= dealer_bit.product
                dealer_bit.status = True
                dealer_bit.save()
                other_bits = Bit.objects.filter(status=farmer_bit,product=product_bit).exclude(pk=dealerbit_id)
                for other_bit in other_bits:
                        other_bit.status='Rejected'
                        other_bit.save()
                return redirect('/farmer/bithistory/')
        except Exception as e:
             return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




def details(request,bitter):
    try:
       user_id = request.session.get('user_id')
       if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
       detail=Users.objects.get(name=bitter)
       bits=Bit.objects.filter(farmer_id=user)
       for bit in bits:
               paid=Paid.objects.filter(user=user,paidfor=bit,paid=True)
       print('paideeee',paid)
       profilepic=Profilepic.objects.get(user=user) 
       return render(request,'details_farmer.html',{'detail':detail,'user_name':user_name,'profilepic':profilepic,'paid':paid})
    except:
       user_id = request.session.get('user_id')
       if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
       detail=Users.objects.get(name=bitter)
       bits=Bit.objects.filter(farmer_id=user)
       for bit in bits:
               paid=Paid.objects.filter(user=user,paidfor=bit,paid=True)
       print('paideeee',paid)
       return render(request,'details_farmer.html',{'detail':detail,'user_name':user_name,'paid':paid})





def wait(request,bitter):
    try:
        user_id=request.session.get('user_id')
        user=Users.objects.get(id=user_id)
        role=user.role
        user_name=user.name
        profilepic=Profilepic.objects.get(user=user)
        paid=Paid.objects.filter(user=user)
        bits=Bit.objects.filter(farmer_id=user,status='True')
        dealername=bitter
        dealer=Users.objects.get(name=dealername)
        dealerpaid=Paid.objects.filter(user=dealer,paid=True)
        if user_id and not paid.exists() and role=="Farmer" and not dealerpaid:
                return render(request,'wait_farmer.html',{'user_name':user_name,'profilepic':profilepic,'bits':bits})
        else:
              user_id = request.session.get('user_id')
              if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
                detail=Users.objects.get(name=bitter)
                bit=Bit.objects.get(bitter=bitter)
                bit_value=bit.bit_value
                quantity=bit.quantity
                quantity=quantity.split()
                amount=(int(bit_value)*int(quantity[0]))/100
                client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
                payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
                print(payment)
                order_id=payment['id']
                order_status=payment['status']
                paid=Paid.objects.filter(user=user,paidfor=bit,paid=True)
                profilepic=Profilepic.objects.get(user=user) 
              return render(request,'details_farmer.html',{'detail':detail,'user_name':user_name,'profilepic':profilepic,'payment':payment,'paid':paid})
    except:
        user_id=request.session.get('user_id')
        user=Users.objects.get(id=user_id)
        role=user.role
        user_name=user.name
        #profilepic=Profilepic.objects.get(user=user)
        paid=Paid.objects.filter(user=user)
        bits=Bit.objects.filter(farmer_id=user,status='True')
        dealername=bitter
        dealer=Users.objects.get(name=dealername)
        dealerpaid=Paid.objects.filter(user=dealer,paid=True)
        if user_id and not paid.exists() and role=="Farmer" and not dealerpaid:
                return render(request,'wait_farmer.html',{'user_name':user_name,'bits':bits})
        else:
              user_id = request.session.get('user_id')
              if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
                detail=Users.objects.get(name=bitter)
                bit=Bit.objects.get(bitter=bitter)
                bit_value=bit.bit_value
                quantity=bit.quantity
                quantity=quantity.split()
                amount=(int(bit_value)*int(quantity[0]))/100
                client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
                payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
                print(payment)
                order_id=payment['id']
                order_status=payment['status']
                paid=Paid.objects.filter(user=user,paidfor=bit,paid=True)
                
              return render(request,'details_farmer.html',{'detail':detail,'user_name':user_name,'payment':payment,'paid':paid})




def farmerpayment_success(request,id,payment_id,order_id,signature,amount,bit_id):
    print('payment_success')
    user_id = request.session.get('user_id')
    user = Users.objects.get(id=user_id)
    bit = Bit.objects.get(id=bit_id)
    bitter=bit.user.name    
    paid = Paid.objects.create(
        user=user,
        paidfor=bit,
        amount=amount,
        razor_pay_order_id=order_id,
        razor_pay_payment_id=payment_id,
        razor_pay_payment_signature=signature,
        paid=True
    )
    paid.save()
    return redirect(f'/farmer/details/{bitter}')
 


def paid(request,amount,id,razorpay_payment_id,razorpay_order_id,razorpay_signature):
       user_id=request.session.get('user_id')
       user=Users.objects.get(id=user_id)
       bit=Bit.objects.filter(farmer_id=user)
       if user_id:
        user = Users.objects.get(id=user_id)
        paid = Paid(
            user=user,
            paidfor=bit,
            amount=amount,
            razor_pay_order_id=razorpay_order_id,
            razor_pay_payment_id=razorpay_payment_id,
            razor_pay_payment_signature=razorpay_signature,
            paid=True
        )
        paid.save()
       bit=Bit.objects.get(farmer_id=user)
       bitter=bit.bitter
       return redirect(f'/farmer/details/{bitter}/')   


def subscription(request):
    user_id = request.session.get('user_id')
    user = Users.objects.get(id=user_id)
    user_name = user.name

    try:
        user_subscription = Subscription.objects.filter(user=user).order_by('planname').first()
    except Subscription.DoesNotExist:
        user_subscription = None

    try:
        profilepic = Profilepic.objects.get(user=user)
    except Profilepic.DoesNotExist:
        profilepic = None

    try:
        freeplan = Free.objects.get(user=user)
    except Free.DoesNotExist:
        freeplan = None

    context = {
        'user_subscription': user_subscription,
        'profilepic': profilepic,
        'user_name': user_name,
        'freeplan': freeplan,
    }
    return render(request, 'subscription_farmer.html', context)




def freeplan(request):          
  try:      
        user_id=request.session.get('user_id')
        user=Users.objects.get(id=user_id)
        amount=0 
        plan='free'     
        sub=Subscription.objects.filter(user=user).order_by('-expiry_date').first()
        date=sub.expiry_date
        expiry_date=date+timedelta(days=3)
        subs=Subscription.objects.create(user=user,planname=plan,expiry_date=expiry_date,date=date,amount=amount,razor_pay_order_id=plan,razor_pay_payment_id=plan,razor_pay_payment_signature=plan,paid=True)
        subs.save()
        freeplan=Free(user=user,free=True)
        freeplan.save()
        return redirect('/farmer/farmerprofile/')
  except:
        user_id=request.session.get('user_id')
        user=Users.objects.get(id=user_id)
        amount=0
        plan='free'     
        current_date = datetime.now().date()
        expiry_date = current_date + timedelta(days=3)
        subs=Subscription.objects.create(user=user,planname=plan,expiry_date=expiry_date,date=current_date,amount=amount,razor_pay_order_id=plan,razor_pay_payment_id=plan,razor_pay_payment_signature=plan,paid=True)
        subs.save()
        freeplan=Free(user=user,free=True)
        freeplan.save()
        return redirect('/farmer/farmerprofile/')





def extendsubscription(request):
    user_id = request.session.get('user_id')
    user = Users.objects.get(id=user_id)
    user_name = user.name

    try:
        user_subscription = Subscription.objects.filter(user=user).order_by('planname').first()
    except Subscription.DoesNotExist:
        user_subscription = None

    try:
        profilepic = Profilepic.objects.get(user=user)
    except Profilepic.DoesNotExist:
        profilepic = None

    try:
        freeplan = Free.objects.get(user=user)
    except Free.DoesNotExist:
        freeplan = None

    context = {
        'user_subscription': user_subscription,
        'profilepic': profilepic,
        'user_name': user_name,
        'freeplan': freeplan,
    }
    return render(request, 'extenedsubscription_farmer.html', context)



def basicplan(request,amount): 
    try: 
        client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
        payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
        print(payment)
        order_id=payment['id']
        order_status=payment['status']
        #if order_status=='created': 
        user_id=request.session.get('user_id')
        user=Users.objects.get(id=user_id)
        user_name=user.name
        profilepic=Profilepic.objects.get(user=user) 
        return render(request,'basicplan_farmer.html',{'payment':payment,'profilepic':profilepic,'user_name':user_name})
    except:
        client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
        payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
        print(payment)
        order_id=payment['id']
        order_status=payment['status']
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        return render(request,'basicplan_farmer.html',{'payment':payment,'user_name':user_name})         
        


def addbasicplan(request,amount):
        user_id=request.session.get('user_id')
        user=Users.objects.get(id=user_id)
        subscribe=Subscription.objects.get(user=user)
        if subscribe:
                new_plan = 'Basic'
                new_duration = 30
                #amount = request.POST.get('amount')

                amount=int(amount)*100
                # Get the current subscription
                current_subscription = Subscription.objects.filter(user=user, paid=True).order_by('-expiry_date').first()
                if current_subscription and current_subscription.expiry_date > timezone.now().date():
                        # Calculate the new expiry date based on the existing subscription
                        new_expiry_date = current_subscription.expiry_date + timedelta(days=new_duration)
                else:
                        # If no current subscription or expired, start from today
                        new_expiry_date = timezone.now().date() + timedelta(days=new_duration)

                # Create a new subscription record
                new_subscription = Subscription(
                        user=user,
                        planname=new_plan,
                        expiry_date=new_expiry_date,
                        date=timezone.now().date(),
                        amount=str(amount),  # Store amount as string in model
                        paid=True,  # Assuming the payment is successful
                        razor_pay_order_id=request.POST.get('razor_pay_order_id', ''),
                        razor_pay_payment_id=request.POST.get('razor_pay_payment_id', ''),
                        razor_pay_payment_signature=request.POST.get('razor_pay_payment_signature', '')
                )
                new_subscription.save()

        else:        
                client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
                payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
                print(payment)
                order_id=payment['id']
                order_status=payment['status']
                #if order_status=='created':
        return render(request,'Productspriceadd_farmer.html')


def standardplan(request,amount):  
    try:        
        client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
        payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
        print(payment)
        order_id=payment['id']
        order_status=payment['status']
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        profilepic=Profilepic.objects.get(user=user) 
        return render(request,'standardplan_farmer.html',{'payment':payment,'profilepic':profilepic,'user_name':user_name})         
    except:
        client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
        payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
        print(payment)
        order_id=payment['id']
        order_status=payment['status']
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        return render(request,'standardplan_farmer.html',{'payment':payment,'user_name':user_name})         


def premiumplan(request,amount):        
    try:
        client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
        payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
        print(payment)
        order_id=payment['id']
        order_status=payment['status']
        #if order_status=='created':
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        profilepic=Profilepic.objects.get(user=user) 
        return render(request,'premiumplan_farmer.html',{'payment':payment,'profilepic':profilepic,'user_name':user_name})
    except:
        client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
        payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
        print(payment)
        order_id=payment['id']
        order_status=payment['status']
        #if order_status=='created':
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        return render(request,'premiumplan_farmer.html',{'payment':payment,'user_name':user_name})





def success(request,amount,payment_id,razorpay_payment_id,razorpay_order_id,razorpay_signature,plan):
        user_id=request.session.get('user_id')
        user=Users.objects.get(id=user_id)
        amount=amount/100       
        if plan.strip() =='basic':
                sub=Subscription.objects.filter(user=user).order_by('-expiry_date').first()
                date=sub.expiry_date
                expiry_date=date+timedelta(days=30)
                subs=Subscription.objects.create(user=user,planname=plan,expiry_date=expiry_date,date=date,amount=amount,razor_pay_order_id=razorpay_order_id,razor_pay_payment_id=razorpay_payment_id,razor_pay_payment_signature=razorpay_signature,paid=True)
                subs.save()
        if plan.strip()=='standard':
                sub=Subscription.objects.filter(user=user).order_by('-expiry_date').first()
                date=sub.expiry_date
                expiry_date=date+timedelta(days=30)
                subs=Subscription.objects.create(user=user,planname=plan,expiry_date=expiry_date,date=date,amount=amount,razor_pay_order_id=razorpay_order_id,razor_pay_payment_id=razorpay_payment_id,razor_pay_payment_signature=razorpay_signature,paid=True)
                subs.save()
        if plan.strip()=='premium':
                sub=Subscription.objects.filter(user=user).order_by('-expiry_date').first()
                date=sub.expiry_date
                expiry_date=date+timedelta(days=30)
                subs=Subscription.objects.create(user=user,planname=plan,expiry_date=expiry_date,date=date,amount=amount,razor_pay_order_id=razorpay_order_id,razor_pay_payment_id=razorpay_payment_id,razor_pay_payment_signature=razorpay_signature,paid=True)
                subs.save()
        return redirect('/farmer/farmerprofile/')




def farmeragreement(request):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')  # Redirect to login if user is not logged in
        
        try:
            user = Users.objects.get(id=user_id)
            user_name = user.name
        except Users.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'User not found.'})

        try:
            profilepic = Profilepic.objects.get(user=user)
        except Profilepic.DoesNotExist:
            profilepic = None  # Handle the case where a user might not have a profile picture
        
        subscriptions = Subscription.objects.filter(user=user)
        if not subscriptions.exists():
            return render(request, 'subscription_farmer.html', {'user_name': user_name, 'profilepic': profilepic})

        product_limit = 0
        for subscription in subscriptions:
            if subscription.planname == 'free':
                product_limit += 1
            elif subscription.planname == 'basic':
                product_limit += 4
            elif subscription.planname == 'standard':
                product_limit += 10
            elif subscription.planname == 'premium':
                product_limit = float('inf')  # Unlimited products for premium plan

            if datetime.now().date() > subscription.expiry_date:
                Product.objects.filter(user=user).delete()
                return render(request, 'subscription_farmer.html', {'user_name': user_name, 'profilepic': profilepic})

        product_count = Product.objects.filter(user=user).count()
        if product_count >= product_limit:
            return render(request, 'cantaddProducts_farmer.html', {
                'fruit_name': '',
                'user_name': user_name,
                'error_message': f'You can add up to {product_limit} products with your current subscriptions.',
                'profilepic': profilepic
            })

        if request.method == "POST":
            product_name = request.POST.get('product_name')
            product_type = request.POST.get('product_type')
            rate = request.POST.get('rate')
            quantity = request.POST.get('quantity')
            quality = request.POST.get('quality')

            if not all([product_name, product_type, rate, quantity, quality]):
                return render(request, 'agreement_farmer.html', {
                    'user_name': user_name,
                    'profilepic': profilepic,
                    'error_message': 'Please fill in all fields.'
                })

            context = {
                'product_name': product_name,
                'product_type': product_type,
                'rate': rate,
                'quantity': quantity,
                'quality': quality,
                'user_name': user_name,
                'profilepic': profilepic,
            }
            return render(request, 'agreement_farmer.html', context)

        return render(request, 'agreement_farmer.html', {'user_name': user_name, 'profilepic': profilepic})

    except Exception as e:
        return render(request, 'cantaddProducts_farmer.html', {'error': f'An unexpected error occurred: {str(e)}'})

   


def farmeragreementdone(request):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/index/')  # Redirect to login if user is not logged in

        try:
            user = Users.objects.get(id=user_id)
            user_name = user.name
        except Users.DoesNotExist:
            return render(request, 'cantaddProducts_farmer.html', {'error': 'User not found.'})

        try:
            profilepic = Profilepic.objects.get(user=user)
        except Profilepic.DoesNotExist:
            profilepic = None  # Handle the case where a user might not have a profile picture

        if request.method == "POST":
            agree = Agreement(user=user, agree=True)
            agree.save()
            return render(request, 'sales_farmer.html', {'user_name': user_name, 'profilepic': profilepic})

        return render(request, 'agreement_farmer.html', {'user_name': user_name, 'profilepic': profilepic})

    except Exception as e:
        return render(request, 'cantaddProducts_farmer.html', {'error': f'An unexpected error occurred: {str(e)}'})




import requests


def get_weather(request):
    user_id=request.session.get('user_id')
    user=Users.objects.get(id=user_id)
    city=user.city
    print(city)
    api_key = 'e23f621c37ff4110916230635241205'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'
    try:
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            return JsonResponse({'error': data['error']['message']}, status=400)
        weather_info = {
            'location': data['location']['name'],
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'humidity': data['current']['humidity'],
            'wind_speed': data['current']['wind_kph'],
            'wind_dir': data['current']['wind_dir'],
            'pressure': data['current']['pressure_mb'],
            'feels_like': data['current']['feelslike_c'],
            'visibility': data['current']['vis_km'],
            'uv_index': data['current']['uv'],
            'cloud': data['current']['cloud'],
            #'sunrise': data['forecast']['forecastday'][0]['astro']['sunrise'],
            #'sunset': data['forecast']['forecastday'][0]['astro']['sunset'],
            # Add more fields as needed
        }
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        profilepic=Profilepic.objects.get(user=user) 
        return render(request,'getweather_farmer.html',{'weather': weather_info,'user_name':user_name,'profilepic':profilepic})
    except :
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            return JsonResponse({'error': data['error']['message']}, status=400)
        weather_info = {
            'location': data['location']['name'],
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'humidity': data['current']['humidity'],
            'wind_speed': data['current']['wind_kph'],
            'wind_dir': data['current']['wind_dir'],
            'pressure': data['current']['pressure_mb'],
            'feels_like': data['current']['feelslike_c'],
            'visibility': data['current']['vis_km'],
            'uv_index': data['current']['uv'],
            'cloud': data['current']['cloud'],
            #'sunrise': data['forecast']['forecastday'][0]['astro']['sunrise'],
            #'sunset': data['forecast']['forecastday'][0]['astro']['sunset'],
            # Add more fields as needed
        }
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        return render(request,'getweather_farmer.html',{'weather': weather_info,'user_name':user_name})
    

