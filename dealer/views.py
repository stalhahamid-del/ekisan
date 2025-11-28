from django.shortcuts import render,redirect
from accounts.models import Users,Subscription,Categories,Crops,Free
from farmer.models import Product,Tracking
from django.shortcuts import render, get_list_or_404
from dealer.models import Bit,DealerProfilepic,DealerBitCounts
from django.http import JsonResponse,HttpResponse
from farmer.models import Message,Paid
import razorpay
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import os
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist



def buy(request):
  try:      
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        categories=Categories.objects.all() 
        profilepic=DealerProfilepic.objects.get(user=user)      
        return render(request,'buy_dealer.html',{'user_name':user_name,'profilepic':profilepic,'categories':categories})
  except:
        user_id = request.session.get('user_id')
        if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
        categories=Categories.objects.all() 
        return render(request,'buy_dealer.html',{'user_name':user_name,'categories':categories})




def addbuy(request):
  try:    
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        user_name = user.name
    profilepic=DealerProfilepic.objects.get(user=user)    
    return render(request, 'addbuy_dealer.html',{'user_name':user_name,'profilepic':profilepic})
  except:
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        user_name = user.name
    return render(request, 'addbuy_dealer.html',{'user_name':user_name})



def crops(request,id):
  try:    
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
        crops_with_farmers = sorted(crops_with_farmers, key=lambda x: x['farmer_count'], reverse=True)

    profilepic=DealerProfilepic.objects.get(user=user)
    return render(request, 'subcategories_dealer.html', {
        'fruit':fruit,
        'user_name': user_name,
        'profilepic':profilepic,
        'crops_with_farmers': crops_with_farmers
    })
  except:
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
        
        crops_with_farmers = sorted(crops_with_farmers, key=lambda x: x['farmer_count'], reverse=True)

    return render(request, 'subcategories_dealer.html', {
        'fruit':fruit,
        'user_name': user_name,
        'crops_with_farmers': crops_with_farmers
    })




def dealersprofile(request):
        try:    
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                profile = Users.objects.get(id=user_id)
                profilepic = None
                subscription=Subscription.objects.filter(user=profile) 
                profilepic=DealerProfilepic.objects.get(user=profile)       
                print('hi',subscription)
                return render(request, 'dealerprofile_dealer.html', {'profile': profile,'profilepic':profilepic,'user_name':user_name,'subscription':subscription})
        except Subscription.DoesNotExist:
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                profile = Users.objects.get(id=user_id)
                profilepic = None
                profilepic=DealerProfilepic.objects.get(user=profile)
                return render(request, 'dealerprofile_dealer.html', {'profile': profile,'profilepic':profilepic,'user_name':user_name,'subscription':subscription})
        except DealerProfilepic.DoesNotExist:
                user_id = request.session.get('user_id')
                user_id = request.session.get('user_id')
                if user_id:
                        user = Users.objects.get(pk=user_id)
                        user_name = user.name
                profile = Users.objects.get(id=user_id)
                profilepic = None
                subscription=Subscription.objects.filter(user=profile)
                return render(request, 'dealerprofile_dealer.html', {'profile': profile,'profilepic':profilepic,'user_name':user_name,'subscription':subscription})
        
        
def editdealerprofile(request,id):
   try:
       user_id = request.session.get('user_id')
       if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
       dealer=Users.objects.get(id=id)
       profilepic=DealerProfilepic.objects.get(user=user)
       return render(request,'editdealerprofile_dealer.html',{'dealer':dealer,'profilepic':profilepic,'user_name':user_name}) 
   except:
       user_id = request.session.get('user_id')
       if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
       dealer=Users.objects.get(id=id)
       return render(request,'editdealerprofile_dealer.html',{'dealer':dealer,'user_name':user_name})             
   

def updatedealerprofile(request,id):
       user=Users.objects.get(id=id)
       if request.method=='POST':
              user.name=request.POST['name']
              user.address=request.POST['address']
              user.city=request.POST['city']
              user.state=request.POST['state']
              user.save()
              return redirect('/dealer/dealerprofile/') 
       return redirect(f'/dealer/editdealerprofile/{id}/') 


def changepassword(request):
  try:  
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = Users.objects.get(id=user_id)
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        password_from_db = user.password
        
        if new_password == confirm_new_password:
                # Verify the current password
                if check_password(current_password, user.password):
                        hashed_password = make_password(new_password)
                        user.password = hashed_password
                        user.save()
                        messages = 'Password successfully changed.'
                        user_id = request.session.get('user_id')
                        if user_id is not None:
                                profile = Users.objects.get(id=user_id)
                                try:        
                                        subscription=Subscription.objects.get(user=user_id)
                                        plantype=subscription.planname
                                        date=subscription.date
                                        expiry_date=subscription.expiry_date
                                        if plantype=='free':
                                                if (subscription is not None):
                                                        profilepic=DealerProfilepic.objects.get(user=user)
                                                        return render(request, 'dealerprofile_dealer.html', {'profile': profile,'profilepic':profilepic,'subscription':subscription,'messages':messages})
                                        else:
                                                expiry_date=date + timedelta(days=30)
                                                if (subscription is not None):
                                                        profilepic=DealerProfilepic.objects.get(user=user)
                                                        return render(request, 'dealerprofile_dealer.html', {'profile': profile,'profilepic':profilepic,'subscription':subscription,'messages':messages})    
                                except ObjectDoesNotExist:
                                        profile = Users.objects.get(id=user_id)
                                        profilepic=DealerProfilepic.objects.get(user=user)
                                        return render(request, 'dealerprofile_dealer.html', {'profile': profile,'profilepic':profilepic,'messages':messages})
                        else:
                                return render(request, 'index.html')   
        return render(request, 'dealerprofile_dealer.html')
  except:
        if request.method == 'POST':
                user_id = request.session.get('user_id')
                user = Users.objects.get(id=user_id)
                current_password = request.POST.get('current_password')
                new_password = request.POST.get('new_password')
                confirm_new_password = request.POST.get('confirm_new_password')
                password_from_db = user.password
                
                if new_password == confirm_new_password:
                        # Verify the current password
                        if check_password(current_password, user.password):
                                hashed_password = make_password(new_password)
                                user.password = hashed_password
                                user.save()
                                messages = 'Password successfully changed.'
                                user_id = request.session.get('user_id')
                                if user_id is not None:
                                        profile = Users.objects.get(id=user_id)
                                        try:        
                                                subscription=Subscription.objects.get(user=user_id)
                                                plantype=subscription.planname
                                                date=subscription.date
                                                expiry_date=subscription.expiry_date
                                                if plantype=='free':
                                                        if (subscription is not None):
                                                                return render(request, 'dealerprofile_dealer.html', {'profile': profile,'subscription':subscription,'messages':messages})
                                                else:
                                                        expiry_date=date + timedelta(days=30)
                                                        if (subscription is not None):
                                                                return render(request, 'dealerprofile_dealer.html', {'profile': profile,'subscription':subscription,'messages':messages})    
                                        except ObjectDoesNotExist:
                                                profile = Users.objects.get(id=user_id)
                                                return render(request, 'dealerprofile_dealer.html', {'profile': profile,'messages':messages})
                                else:
                                        return render(request, 'index.html')   
                return render(request, 'dealerprofile_dealer.html')





def dealerprofilepic(request):
    if request.method == 'POST' and request.FILES.get('profilepic'):
        user_id = request.session.get('user_id')
        user = Users.objects.get(id=user_id) 
        profile, created = DealerProfilepic.objects.get_or_create(user=user)
        
        profile.profilepic = request.FILES['profilepic']
        profile.save()
        
        return redirect('/dealer/dealersprofile/')
    return redirect('/dealer/dealersprofile/')





def productcategory(request):
  try:
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        user_name = user.name  
    profilepic=DealerProfilepic.objects.get(user=user) 
    return render(request, 'productcategory_dealer.html',{'user_name':user_name,'profilepic':profilepic})
  except:
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        user_name = user.name  
    return render(request, 'productcategory_dealer.html',{'user_name':user_name})   




def productcategorylist(request):
  try:
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        user_name = user.name   
    user=Users.objects.get(id=user_id)
    name=user.name
    products=Bit.objects.filter(bitter=name,status=True) 
    print(products)  
    profilepic=DealerProfilepic.objects.get(user=user)
    return render(request, 'productcategorylist_dealer.html',{'user_name':user_name,'profilepic':profilepic,'products':products})
  except:
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        user_name = user.name   
    user=Users.objects.get(id=user_id)
    name=user.name
    products=Bit.objects.filter(bitter=name,status=True) 
    print(products)  
    return render(request, 'productcategorylist_dealer.html',{'user_name':user_name,'products':products})

   

        
def productlist(request, fruit):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/index/') 
        user = Users.objects.get(pk=user_id)
        user_name = user.name

        try:
            bit = Bit.objects.get(product=fruit, status=True)
            fruit_data = []  
        except Bit.DoesNotExist:
            fruit_data = get_list_or_404(Product, product_name=fruit)

        profilepic = DealerProfilepic.objects.get(user=user)
        return render(request, 'productlist_dealer.html', {
            'fruit_data': fruit_data,
            'profilepic': profilepic,
            'fruit': fruit,
            'user_name': user_name
        })

    except Http404:
        fruit_data = []
        user_id = request.session.get('user_id')
        if user_id:
            user = Users.objects.get(pk=user_id)
            user_name = user.name
        else:
            user_name = ""

        return render(request, 'productlist_dealer.html', {
            'fruit_data': fruit_data,
            'fruit': fruit,
            'user_name': user_name
        })

    except Users.DoesNotExist:
        return redirect('/index/')  

    except DealerProfilepic.DoesNotExist:
        profilepic = None

        return render(request, 'productlist_dealer.html', {
            'fruit_data': fruit_data,
            'profilepic': profilepic,
            'fruit': fruit,
            'user_name': user_name
        })

    except Exception as e:
        user_id = request.session.get('user_id')
        if user_id:
            user = Users.objects.get(pk=user_id)
            user_name = user.name
        else:
            user_name = ""

        return render(request, 'productlist_dealer.html', {
            'fruit_data': [],
            'fruit': fruit,
            'user_name': user_name
        })





def bit(request, user_id, user_name, product_name, product_type, quality, rate, quantity):
  try:
     name=user_name
     user_id=request.session.get('user_id')
     user=Users.objects.get(id=user_id)
     user_name="" 
     user_name=user.name  
     profilepic=DealerProfilepic.objects.get(user=user)
     context = {
        'user_id': user_id,     
        'user_name': user_name,
        'product_name': product_name,
        'product_type': product_type,
        'quality': quality,
        'rate': rate,
        'quantity': quantity,
        'profilepic':profilepic
    }
     return render(request,'bit_dealer.html',context)
  except:
     name=user_name
     user_id=request.session.get('user_id')
     user=Users.objects.get(id=user_id)
     user_name="" 
     user_name=user.name  
     context = {
        'user_id': user_id,     
        'user_name': user_name,
        'product_name': product_name,
        'product_type': product_type,
        'quality': quality,
        'rate': rate,
        'quantity': quantity,
        }
     return render(request,'bit_dealer.html',context)



from django.shortcuts import get_object_or_404, render
from django.utils import timezone

def process_bit(request, user_id, user_name, product_name, product_type, quality, rate, quantity):
    try:
        if request.method == "POST":
            bit_value = request.POST.get('bit', None)
            if bit_value is None:
                return render(request, 'cantBuy_dealer.html', {
                    'error_message': 'No bit value provided.',
                    'user_name': user_name
                })
        else:
            return render(request, 'cantBuy_dealer.html', {
                'error_message': 'Invalid request method.',
                'user_name': user_name
            })

        user = get_object_or_404(Users, id=user_id)
        user_name = user.name

        # Check for Profilepic
        profilepic = DealerProfilepic.objects.filter(user=user).first()

        current_date = timezone.now().date()
        subscriptions = Subscription.objects.filter(user=user, expiry_date__gte=current_date)

        if not subscriptions.exists():
            return render(request, 'cantBuy_dealer.html', {
                'error_message': 'You do not have an active subscription.',
                'profilepic': profilepic,
                'user_name': user_name
            })

        # Calculate the total number of bits the dealer can make
        total_bits_allowed = 0
        unlimited = False

        for subscription in subscriptions:
            if subscription.planname == 'free':
                total_bits_allowed += 1
            elif subscription.planname == 'basic':
                total_bits_allowed += 4
            elif subscription.planname == 'standard':
                total_bits_allowed += 10
            elif subscription.planname == 'premium':
                unlimited = True
                break  # No need to check further if premium subscription is found

        if unlimited:
            total_bits_allowed = float('inf')  # Unlimited bits

        dealer_bit_count, created = DealerBitCounts.objects.get_or_create(user=user)

        if dealer_bit_count.current_bid_count >= total_bits_allowed and not unlimited:
            return render(request, 'cantBuy_dealer.html', {
                'error_message': f'You can buy only {total_bits_allowed} bits based on your subscriptions.',
                'profilepic': profilepic,
                'user_name': user_name
            })

        # Check if a bit already exists for this product by the same dealer
        existing_bit = Bit.objects.filter(
            farmer=user_name, 
            product=product_name, 
            bitter=user_name
        ).first()
        
        if existing_bit:
            return render(request, 'cantBuy_dealer.html', {
                'error_message': 'You have already created a bit for this product.',
                'profilepic': profilepic,
                'user_name': user_name
            })

        farmer = get_object_or_404(Users, name=user_name)
        address = farmer.address

        bitter = get_object_or_404(Users, id=user_id)
        bittername = bitter.name
        bitteraddress = bitter.address

        # Create Bit
        bit = Bit.objects.create(
            farmer_id=user,
            farmer=user_name,
            farmer_address=address,
            product=product_name,
            product_type=product_type,
            quality=quality,
            rate=rate,
            quantity=quantity,
            bit_value=bit_value,
            bitter=bittername,
            bitter_address=bitteraddress
        )

        dealer_bit_count.current_bid_count += 1
        dealer_bit_count.save()

        return redirect('/dealer/mybits/')

    except Free.DoesNotExist:
        profilepic = DealerProfilepic.objects.filter(user=user).first()
        return render(request, 'cantBuy_dealer.html', {
            'profilepic': profilepic,
            'user_name': user_name
        })

    except DealerProfilepic.DoesNotExist:
        return render(request, 'cantBuy_dealer.html', {
            'error_message': 'Profile picture not found.',
            'user_name': user_name
        })

    except Subscription.DoesNotExist:
        profilepic = DealerProfilepic.objects.filter(user=user).first()
        return render(request, 'cantBuy_dealer.html', {
            'error_message': 'No active subscription found.',
            'profilepic': profilepic,
            'user_name': user_name
        })

    except Exception as e:
        return render(request, 'cantBuy_dealer.html', {
            'error_message': str(e),
            'user_name': user_name
        })




def mybits(request):
        try:
            user_id = request.session.get('user_id')
            user = Users.objects.get(id=user_id)
            name=user.name
            if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
            bit_data = Bit.objects.filter(bitter=name).values('product','farmer', 'product_type', 'quantity', 'rate', 'quality', 'bit_value')
            print('het',bit_data)
            bit = {}
            for entry in bit_data:
                product_name = entry['product']
                if product_name not in bit or product_name in bit:
                        bit[product_name] = []
                        bit[product_name].append(entry)
            
            notifications = Message.objects.filter(user=user)
            profilepic=DealerProfilepic.objects.get(user=user)    
            context = {
                        'bit': bit,
                        'bit_data':bit_data,
                        'user_name':user_name,
                        'notifications':notifications,
                        'profilepic':profilepic
                }
            print(context)
            return render(request,'mybits_dealer.html',context)
        except DealerProfilepic.DoesNotExist:
            user_id = request.session.get('user_id')
            user = Users.objects.get(id=user_id)
            name=user.name
            if user_id:
                user = Users.objects.get(pk=user_id)
                user_name = user.name
            bit_data = Bit.objects.filter(bitter=name).values('product','farmer', 'product_type', 'quantity', 'rate', 'quality', 'bit_value')
            print('het',bit_data)
            bit = {}
            for entry in bit_data:
                product_name = entry['product']
                if product_name not in bit or product_name in bit:
                        bit[product_name] = []
                        bit[product_name].append(entry)
            
            notifications = Message.objects.filter(user=user)
            context = {
                        'bit': bit,
                        'bit_data':bit_data,
                        'user_name':user_name,
                        'notifications':notifications,
                }
            print(context)
            return render(request,'mybits_dealer.html',context)
        except Bit.DoesNotExist:
                return render(request, 'error.html', {'message': 'Bit not found'})
        




def get_notifications(request):
        try:
            id=request.session.get('user_id')
            user = Users.objects.get(id=id)
            user_notifications = Message.objects.filter(user=user.name).values('notification', 'product')
            notifications = [{'notification': notification['notification'], 'product': notification['product']} for notification in user_notifications]
            bit_value = Bit.objects.filter(bitter=user.name)
            for bit_value in bit_value:    
                quantity = bit_value.quantity
            return JsonResponse({'notifications': notifications, 'bit_value': bit_value.bit_value, 'quantity': quantity})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Bit object does not exist for the current user'})
        


def pay(request,amount,name,quantity):
  try:
    charge=amount*0.05
    quantity_numeric = float(''.join(filter(str.isdigit, quantity)))
    yourAmount=amount
    amount=amount*quantity_numeric
    charge=charge*quantity_numeric
    client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
    payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
    user_id=request.session.get('user_id')
    user=Users.objects.get(id=user_id)
    address=user.address
    user_name = user.name
    paymentAmount=amount*quantity_numeric
    delivery_charge=yourAmount*0.10*quantity_numeric
    total=amount+charge+delivery_charge
    pay=total*100
    profilepic=DealerProfilepic.objects.get(user=user)
    return render(request,'payments_dealer.html',{'total':total,'pay':pay,'amount':amount,'quantity':quantity,'yourAmount':yourAmount,'paymentAmount':paymentAmount,'delivery_charge':delivery_charge,'charge':charge,'name':name,'address':address,'user_name':user_name,'profilepic':profilepic})
  except:
    charge=amount*0.05
    quantity_numeric = float(''.join(filter(str.isdigit, quantity)))
    yourAmount=amount
    amount=amount*quantity_numeric
    charge=charge*quantity_numeric
    client = razorpay.Client(auth=('rzp_test_bX75Gd98qBwkpY', 'dqDmwLhAXqBPTz1okdtBUHMJ'))
    payment = client.order.create({'amount':(amount)*100,'currency':"INR",'payment_capture':'1'})
    user_id=request.session.get('user_id')
    user=Users.objects.get(id=user_id)
    address=user.address
    user_name = user.name
    paymentAmount=amount*quantity_numeric
    delivery_charge=yourAmount*0.10*quantity_numeric
    total=amount+charge+delivery_charge
    pay=total*100
    return render(request,'payments_dealer.html',{'total':total,'pay':pay,'amount':amount,'quantity':quantity,'yourAmount':yourAmount,'paymentAmount':paymentAmount,'delivery_charge':delivery_charge,'charge':charge,'name':name,'address':address,'user_name':user_name})




def payment_success(request,id,payment_id,order_id,signature,amount,bit_id):
    user_id = request.session.get('user_id')
    user = Users.objects.get(id=user_id)
    bit = Bit.objects.get(id=bit_id)

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
    return redirect('/dealer/mybits/')






def subscription(request):
  try:    
    user_id = request.session.get('user_id')
    user=Users.objects.get(id=user_id)    
    current_date = timezone.now().date()
    has_subscription = Subscription.objects.filter(user=user, expiry_date__gte=current_date, paid=True).exists()
    has_free_plan = Free.objects.filter(user=user, free=True).exists()
    if has_subscription or has_free_plan:
        return redirect('/dealer/dealersprofile/')
    else:
        user_id = request.session.get('user_id')
        user=Users.objects.get(id=user_id) 
        user_name=user.name   
        profilepic=DealerProfilepic.objects.get(user=user)
        return render(request,'subscription_dealer.html',{'user_name':user_name,'profilepic':profilepic})                              
  except:
    user_id = request.session.get('user_id')
    user=Users.objects.get(id=user_id)    
    current_date = timezone.now().date()
    has_subscription = Subscription.objects.filter(user=user, expiry_date__gte=current_date, paid=True).exists()
    has_free_plan = Free.objects.filter(user=user, free=True).exists()
    if has_subscription or has_free_plan:
        return redirect('/dealer/dealersprofile/')
    else:
        user_id = request.session.get('user_id')
        user=Users.objects.get(id=user_id) 
        user_name=user.name   
        return render(request,'subscription_dealer.html',{'user_name':user_name})                              
        



def extendsubscription(request):
    user_id = request.session.get('user_id')
    user = Users.objects.get(id=user_id)
    user_name = user.name

    try:
        user_subscription = Subscription.objects.filter(user=user).order_by('planname').first()
    except Subscription.DoesNotExist:
        user_subscription = None

    try:
        profilepic = DealerProfilepic.objects.get(user=user)
    except DealerProfilepic.DoesNotExist:
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
    return render(request, 'extendedsubscription_dealer.html', context)



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
        return redirect('/dealer/dealersprofile/')
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
        return redirect('/dealer/dealersprofile/')




def basicplan(request,amount): 
  try:       
        print((amount))
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
        
        profilepic=DealerProfilepic.objects.get(user=user) 
        return render(request,'basicplan_dealer.html',{'payment':payment,'profilepic':profilepic,'user_name':user_name})
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
        
        return render(request,'basicplan_dealer.html',{'payment':payment,'user_name':user_name})



def standardplan(request,amount):
  try:        
        print((amount))
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
        profilepic=DealerProfilepic.objects.get(user=user) 
        return render(request,'standardplan_dealer.html',{'payment':payment,'profilepic':profilepic,'user_name':user_name})         
  except:
        print((amount))
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
        return render(request,'standardplan_dealer.html',{'payment':payment,'user_name':user_name})         





def premiumplan(request,amount):  
  try:      
        print((amount))
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
        profilepic=DealerProfilepic.objects.get(user=user) 
        return render(request,'premiumplan_dealer.html',{'payment':payment,'profilepic':profilepic,'user_name':user_name})
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
        return render(request,'premiumplan_dealer.html',{'payment':payment,'user_name':user_name})


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
        return redirect('/dealer/dealersprofile/')


