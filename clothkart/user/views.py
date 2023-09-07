from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,logout,login
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm,UserProfileForm,UserForm,CustomercareForm,ReturnForm,RefundForm
from .models import User
from store.models import Customer_care
# from orders.models import Order, OrderProduct
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from addcart.views import _cart_id
from addcart.models import Cart, CartItem
import requests
from addcart.models import Cart
from order.models import Order,OrderProduct
import socket
from.models import User,UserProfile
from order.models import SupplierShipment,Return

from datetime import datetime, timedelta
import datetime
socket.getaddrinfo('localhost',8080)
# socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0)
addressInfo = socket.getaddrinfo("localhost", 8080, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
# socket_ = socket.create_connection(('localhost', 8080), 1)
# host, port = self.bind_addr
# try:
#     if type(host) is not str:
#        return 
#     info = socket.getaddrinfo(host, port, socket.AF_UNSPEC,
#                             socket.SOCK_STREAM, 0, socket.AI_PASSIVE)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
        
            user.save()
            
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # activetion user
            current_site=get_current_site(request)
            mail_subject='Please active your account'
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email=email
            send_email= EmailMessage('Please active your account',message,to=[to_email])
            # send_email.send()
            # return redirect('/user/login/?command=verification&email='+email)
            return redirect('login')
        
           
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            # messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                    if user.roll == "admin":
                        return redirect('add_product')
                    elif user.roll == "supplier":
                        return redirect('view_supplier_order_detail')
          
                    elif user.roll == "mainagent":
                        return redirect('addcorporateagent')
          
                    elif user.roll == "subagent":
                        return redirect('corporateagent_view')
          
                    else:
                        return redirect('home')
          
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')




def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()


    context = {
        'orders_count': orders_count,
      
    }
    return render(request, 'accounts/dashboard.html',context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


def index(request):  
    send_mail(
            'Subject here',
            'Here is the message.',
            'ishwarya.ideaux@gmail.com',
            ['ishwaryaravi2001@gmail.com'],
            fail_silently=False,
    )
    return render(request,'accounts/index.html')

@login_required(login_url='login')
def my_order(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)




@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
            user_form = UserForm(instance=request.user)
            profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id,ordered=True)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


def orders_detail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id,ordered =True)
    order = Order.objects.get(order_number=order_id)
    orde=OrderProduct.objects.filter(order_id=order.id,ordered =True)
    print(orde)
    
    # for i in orde:
    #     print(i)
    #     if i.delivered_date != None:
    #         product=i.product_id
    #         print(product)
    #         date=i.delivered_date
    #         # s=i.checking_date
    #         # print(s)
    #         print(date)
    #         # d=datetime.datetime(2023,3,9)
    #         # print(type(d))
    #         da=[]
    #         for i in range(8): 
    #             date += datetime.timedelta(days=1)
    #             da.append(date)
    #         d=da[-1]
            
    #         print(d)
    #         print(type(d))
    #         date_time= datetime.datetime.strftime(d, '%Y-%m-%d')
    #         print(date_time)
    #         print(type(date_time))
    #         x=datetime.datetime.now().strftime ("%Y-%m-%d")
    #         print(type(x))
            

    #         if date_time >= x:
    #             i.is_reached = 1
    #             print("fuytguyt8i")
    #             i.save()
    #         else:
    #             print("Not reached")
    #     else:
    #         print("df")
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/orders_detail.html',context)


def return_detail(request,id):
    return_detail=OrderProduct.objects.get(id=id)
    order=Order.objects.get(id= return_detail.order_id)
    order_product=OrderProduct.objects.filter(order_id=order.id)
    subtotal=0
    date=return_detail.delivered_date

    for i in order_product:
        subtotal+=  i.product_price * i.quantity
    # da=[]
    # for i in range(8):
    #     date += datetime.timedelta(days=1)
    #     da.append(date)
    # d=da[-1]
    # current_datetime=datetime.datetime.now
    # if current_datetime==d:
    #     return_detail.is_reached=True
    #     return_detail.save()
    #     return render(request, 'accounts/return.html',{'return_detail':return_detail,'subtotal':subtotal})
    # else:
        # return_detail.is_reached=False
        # return_detail.save()
        # return render(request, 'accounts/return.html',{'return_detail':return_detail,'subtotal':subtotal})


    return render(request, 'accounts/return.html',{'return_detail':return_detail,'subtotal':subtotal})




def order_tract_detail(request,id):
      order = OrderProduct.objects.get(id=id)
      track_detail = SupplierShipment.objects.filter(order_id=order.order_id, product_id = order.product.id )

      return render(request, 'accounts/order_track_detail.html',{'track_detail':track_detail})

def cancel_order_request(request,id):
    order_product=OrderProduct.objects.get(id=id)
    order_id=order_product.order.order_number
    current_site=get_current_site(request)
    order_product.is_order=False
    order_product.cancel_status="Cancellation_requested"
    order_product.save()
    # messages.success(request,'Order product cancelletaion request submitted')
    # return redirect("http://"+f'{current_site}'+"user/orders_detail/"+f'{order_id}/')
    return redirect("http://"+f'{current_site}'+"/user/orders_detail/"+f'{order_id}')



def customer_care(request):
    user=request.user
    y=Customer_care.objects.all()
    if request.method == "POST":
        form=CustomercareForm(request.POST)
        if form.is_valid():
            x=form.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            ticket = current_date + str(x.id)
            x.ticket=ticket
            x.user=user
            x.save()
            messages.success(request,"Thank you for contacting us we will review it and get back to you !")
            return render (request,'accounts/customer_care.html',{'y':y})
        else:
            return render (request,'accounts/customer_care.html',{'y':y,'form':form})
    return render (request,'accounts/customer_care.html',{'y':y})



def order_return(request,id):
    order=OrderProduct.objects.get(id=id)
    print(order)
    form=ReturnForm()
    current_site=get_current_site(request)
    if request.method == "POST":
        form = ReturnForm(request.POST)
        reason=request.POST.get('reason')
        if form.is_valid():
            x=form.save()
            x.order_id=order.id

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            return_id = current_date + str(x.id)
          
            x.return_id=return_id
            x.save()
            z=OrderProduct.objects.get(id=x.order_id)
            date=z.delivered_date
            y= date+timedelta(days=15)
            print(y)
            x.return_pickup_date = y
            x.save()
            print(order.order_id)
            id=x.id
            return redirect("http://"+f'{current_site}'+"/user/add_account/"+f'{id}')

        else:
           return render (request,'accounts/return_request.html',{'order':order,'form':form,'reason':reason})
    return render (request,'accounts/return_request.html',{'order':order})

def add_account(request,id):
    print(id)
   
    refund=Return.objects.get(id=id)
    print(refund)
    # id=refund.order
    id=refund.id
    form=RefundForm()
    current_site=get_current_site(request)
    if request.method == "POST":
        
      
        form = RefundForm(request.POST)
        if form.is_valid():
            account_no=request.POST.get('account_no')
            confirm_account_no=request.POST.get('confirm_account_no')
            ifscno=request.POST.get('ifscno')
            account_holder_name=request.POST.get('account_holder_name')
            
            if account_no != confirm_account_no:
                error= "Account number does not match"
                return render (request,'accounts/add_account.html',{'form':form,'error':error})
            else:
                 refund.account_no=account_no
                 refund.confirm_account_no=confirm_account_no
                 refund.ifscno=ifscno
                 refund.account_holder_name=account_holder_name
                 refund.return_status = "return_requested"
                #  refund.admin_return_status ="return_requested"
                #  messages.success(request,"return request submitted successfully")
                 refund.save()
                 
                 return redirect("http://"+f'{current_site}'+"/user/return_complete/"+f'{id}')
          

        else:
           return render (request,'accounts/add_account.html',{'form':form})
    return render (request,'accounts/add_account.html')


def return_complete(request,id):
    return_obj= Return.objects.get(id=id)
  
    z=OrderProduct.objects.get(id=return_obj.order_id)
    z.return_status="return_requested"
    z.save()
    x=z.delivered_date
    y=x+timedelta(days=15)
    print(y)
    return render(request,'accounts/return_complete.html',{'return_obj':return_obj,'y':y})
