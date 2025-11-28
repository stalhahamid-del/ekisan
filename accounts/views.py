from django.shortcuts import render,redirect,HttpResponse
from accounts.models import Users,Profilepic,Crops,Categories
from dealer.models import DealerProfilepic
from farmer.models import Product,Message
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.db.models import Count
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.conf import settings
from twilio.rest import Client
from cryptography.fernet import Fernet

# Create your views here.

def home(request):
    farmers = Users.objects.filter(role='Farmer')[:6]
    profilepic = {}   
    for farmer in farmers:
        profilepic[farmer] = Profilepic.objects.filter(user=farmer).first()
    dealers = Users.objects.filter(role='Dealer')[:6]
    dealerprofilepic = {}   
    for dealer in dealers:
        dealerprofilepic[dealer] = DealerProfilepic.objects.filter(user=dealer).first()
    total_messages = Message.objects.count()
    latest_messages = Message.objects.all()[max(total_messages - 3, 0):]
    distinct_product_names = Product.objects.values('product_name').distinct()
    products_info = Product.objects.values('product_name').distinct().annotate(
        total_quantity=Sum('quantity'),
        total_rate=Sum('rate')
    )
    product_crops_dict = {}
    for product_info in products_info:
        product_name = product_info['product_name']
        products = Product.objects.filter(product_name=product_name)
        crops = Crops.objects.filter(nameineng=product_name)
        product_crops_dict[product_name] = {
            'products': products,
            'product_info': product_info,
            'crops': crops
        }
    print("farmers",farmers,'profilepic',profilepic,'dealers',dealers,'dealerprofilepic',dealerprofilepic,'products_info',products_info,'latest_messages',latest_messages,'product_crops_dict',product_crops_dict)
    return render(request, 'home_accounts.html', {
        'farmers': farmers,
        'profilepic': profilepic,
        'dealers': dealers,
        'dealerprofilepic': dealerprofilepic,
        'products_info': products_info,
        'latest_messages': latest_messages,
        'product_crops_dict': product_crops_dict
    })




def privacypolicy(request):
    return render(request,'privacypolicy.html')

def termsandconditons(request):
    return render(request,'termsandconditons.html')

def aboutus(request):
    return render(request,'aboutus_accounts.html')



def forget(request):
    if request.method=="POST":
        mobile=request.POST['mobile']
        mobile_exists=Users.objects.get(mobile=mobile)
        if mobile_exists:
            try:
                user=Users.objects.get(mobile=mobile)        
            except Users.DoesNotExist:
                return render(request, 'forget_accounts.html', {'error': 'User with this mobile does not exist.'})

            encrypted_password = user.password
            encrypted_password = encrypted_password[2:-1]
            key = settings.FERNET_KEY
            cipher_suite = Fernet(key)
            try:
                decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            except Exception as e:
                return render(request, 'forget_accounts.html', {'error': 'Error decrypting password.'})

            name=user.name

            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            from_phone = settings.TWILIO_PHONE_NUMBER
            to_phone = f"+91{mobile}"

            client = Client(account_sid, auth_token)
            message_body = f"\nDear {name}, \nYour EKISAN password is {decrypted_password}."
            try:
                client.messages.create(
                    body=message_body,
                    from_=from_phone,
                    to=to_phone
                )
                return redirect('/index/')
            except Exception as e:
                return render(request, 'forget_accounts.html', {'error': f'Error sending SMS: {e}'})
        else:
            return render(request,'forget_accounts.html')            
    return render(request,'forget_accounts.html')




# def index(request):
#     if request.method == "POST":
#         mobile = request.POST.get('mobile')
#         password = request.POST.get('password')
#         user = Users.objects.filter(mobile=mobile).first()
#         if user is not None:
#             # encrypted_password = user.password
#             # encrypted_password = encrypted_password[1:]
#             # encrypted_password = encrypted_password  # Ensure it's bytes
#             # key = settings.FERNET_KEY  # Ensure the key is bytes
#             # cipher_suite = Fernet(key)
#             # decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
#             # print('decrypted_password',decrypted_password)
#             decrypted_password = check_password(password,user.password)
#             if password == decrypted_password:
#                 if user is not None:    
#                     if user.role == 'Farmer':
#                         request.session['user_id'] = user.id
#                         request.session['user_role'] = 'Farmer'
#                         return redirect('/farmer/subscription/')
#                     elif user.role == 'Dealer':
#                         request.session['user_id'] = user.id
#                         request.session['user_role'] = 'Dealer'
#                         return redirect('/dealer/subscription/')
                    
#                 else:
#                     return render(request, 'index_accounts.html')
#             else:
#                     return render(request, 'index_accounts.html',{'error':'Password or Mobile not correct'})
#         else:
#             return render(request, 'index_accounts.html')    
#     else:
#         return render(request, 'index_accounts.html')    
                

def index(request):
    print("HIIII")
    if request.method == "POST":
        print("HEYYYY")
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        print("mobile",mobile)
        print("password",password)

        # Check if user exists
        user = Users.objects.filter(mobile=mobile).first()

        if not user:
            messages.error(request, "Mobile number not registered")
            return render(request, 'index_accounts.html')

        # Check password
        if password!= user.password:
            messages.error(request, "Incorrect password")
            print('user',user.password)
            return render(request, 'index_accounts.html')

        # Login success
        request.session['user_id'] = user.id
        request.session['user_role'] = user.role

        # Redirect based on role
        if user.role == 'Farmer':
            return redirect('/farmer/subscription/')
        else:
            return redirect('/dealer/subscription/')

    return render(request, 'index_accounts.html')

        

def otp(request):
    return render(request, 'otp_accounts.html')




from django.shortcuts import render, redirect
from django.contrib import messages
from .mixins import MessageHandler
import random

# def register(request):
#     if request.method == "POST":
#         mobile = request.POST.get('mobile')
#         try:
#             # Check if the mobile number already exists
#             mobile_exists = Users.objects.get(mobile=mobile)
#             messages.error(request, 'Mobile number already registered.')
#             return render(request, 'register_accounts.html')
#         except Users.DoesNotExist:
#             # Mobile number does not exist, proceed with registration
#             name = request.POST.get('name')
#             password = request.POST.get('password')
#             state = request.POST.get('state')
#             city = request.POST.get('city')
#             address = request.POST.get('address')
#             role = request.POST.get('role')
#             pincode = request.POST.get('pincode')
#             mobile = '+91' + mobile 
            
#             # Generate OTP
#             otp = random.randint(100000, 999999)
#             message_handler = MessageHandler(phone_number=mobile, otp=otp)
#             message_handler.send_otp_on_phone()
            
#             # Store registration data and OTP in session
#             request.session['registration_data'] = {
#                 'name': name,
#                 'mobile': mobile,
#                 'password': password,
#                 'state': state,
#                 'city': city,
#                 'address': address,
#                 'role': role,
#                 'pincode': pincode,
#             }

#             request.session['otp'] = otp
#             return redirect('/otp/')
#     else:
#         return render(request, 'register_accounts.html')

def register(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')

        # Check if mobile already registered
        if Users.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Mobile number already registered.')
            return render(request, 'register_accounts.html')

        # Gather form data
        name = request.POST.get('name')
        password = request.POST.get('password')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        role = request.POST.get('role')
        pincode = request.POST.get('pincode')

        # Create user directly
        user = Users.objects.create(
            name=name,
            mobile=mobile,
            password=password,
            state=state,
            city=city,
            address=address,
            role=role,
            pincode=pincode
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('/index/')

    return render(request, 'register_accounts.html')
   
   
def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp_value')
        otp_session = request.session.get('otp')
        print('verify',otp_input,otp_session)
        if otp_input == str(otp_session):
            registration_data = request.session.get('registration_data')
            name = registration_data.get('name')
            mobile = registration_data.get('mobile')
            if mobile and mobile.startswith('+91'):
                mobile = mobile[3:]
            password = registration_data.get('password')
            state = registration_data.get('state')
            city = registration_data.get('city')
            address = registration_data.get('address')
            role = registration_data.get('role')
            pincode = registration_data.get('pincode')
            valid_roles = ['Farmer', 'Dealer']  
            if role not in valid_roles:
                return render(request, 'register_accounts.html', {'error_message': 'Invalid role'})
            
            # key = settings.FERNET_KEY
            # print('keyencryption',key)
            # cipher_suite = Fernet(key)
            # encrypted_password = cipher_suite.encrypt(password.encode())

            encrypted_password = make_password(password)
            username=name.lower()
            
            user = Users(name=name,username=username,address=address,state=state,city=city,pincode=pincode,mobile=mobile,password=encrypted_password ,role=role)
            user.save()
            request.session.pop('registration_data', None)
            request.session.pop('otp', None)
            messages.success(request, 'Registration successful!')
            return redirect('/index/') 
        else:
            messages.error(request, 'Invalid OTP, please try again.')    
    return render(request, 'otp_accounts.html')



def logout(request):
    django_logout(request)
    request.session.flush()
    
    return redirect('/')

