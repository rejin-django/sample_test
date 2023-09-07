from django.shortcuts import render,redirect
from.forms import SupplierShipmentForm,Product_Form,Category_Form,Variation_Form,Product_gallery_Form,Supplier_Form,Corporate_Form,MainAgent_Form
from store.models import Category,Variation,ProductGallery,Supplier
from cart.models import Category
from store.models import Product
from order.forms import SalesmanForm
from order.models import Salesman
from order.models import Order,Payment,CorporateAgent,Shipment,SupplierShipment,Salesman,MainAgent
import hashlib
from django.http import HttpResponse
from store.models import Customer_care
from .models import customer_Solution
from .forms import Customer_solution_Form
from django.db.models import Sum
from django.db.models.functions import TruncMonth ,TruncYear
import datetime
from django.contrib import messages
from order.models import OrderProduct,Order,State,District,Return
from datetime import date
from .forms import About_Product_Form
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from user.models import User
from django.contrib.sites.shortcuts import get_current_site
# date object of today's date

 


# Create your views here.
def staff_home(request):
    # months = date.today().month
    # print(months)
    # x=Payment.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total_amount=Sum('amount_paid'))
    # for i in x :
    #    if i.month == months :
    #     print(i.amount_paid)

    return render(request,'admin/home.html')
def product(request):
   return render(request,'admin/product.html')

def add_product(request):
    form= Product_Form() 
    y=Product.objects.all().order_by('-created_date')
    x=Category.objects.all()
    supplier=Supplier.objects.all()
    if request.method=="POST":
        y=Product.objects.all().order_by('-created_date')
        form= Product_Form(request.POST,request.FILES) 
        category= request.POST.get('category')
        suppliers= request.POST.get('supplier')
        if form.is_valid():

            brand= request.POST.get('brand')
            mrp= request.POST.get('mrp')
            price= request.POST.get('price')
            if int(mrp) < int(price):
             
              error=["product price should be less than mrp price"]
              print(error)
              return render(request,'admin/add_product.html',{'form':form,'x':x,'y':y,'supplier':supplier,'error':error,'suppliers':suppliers,'category':category}) 

            else:

                off = (int(mrp) - int(price)) * 100
                offer=off/ int(mrp)
                t=form.save()
                t.offer=offer
                t.save()
                messages.success(request,'Product added successfully')
                return redirect('add_product') 
        else:
           return render(request,'admin/add_product.html',{'form':form,'x':x,'y':y,'supplier':supplier,'suppliers':suppliers,'category':category})   
    return render(request,'admin/add_product.html',{'form':form,'x':x,'y':y,'supplier':supplier})

def add_category(request):
    form=Category_Form()
    x=Category.objects.all()
    if request.method=="POST":
        x=Category.objects.all()
        form= Category_Form(request.POST,request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request,'Product category added successfully')
            return render(request,'admin/add_category.html',{'x':x})
        else:
            print(form.errors)
            return render(request,'admin/add_category.html',{'form':form,'x':x})
    return render(request,'admin/add_category.html',{'form':form,'x':x})


def add_product_variation(request):
    form=Variation_Form()
    x=Product.objects.filter(is_available=True).order_by('-created_date')
    y=Variation.objects.all()
    if request.method=="POST":
        y=Variation.objects.all()
        form= Variation_Form(request.POST,request.FILES) 
        product_name=request.POST.get('product')
        variation_category= request.POST.get('variation_category')
        variation_value= request.POST.get('variation_value')
        if form.is_valid():
            id=request.POST.get('product')
            product=Product.objects.get(id=id)
           
            variation= Variation.objects.filter(product=product,variation_category=variation_category,variation_value=variation_value)
            if variation :
                messages.error(request,'product' + f'{variation_category}' + "  :  " + f'{variation_value}' + 'variation already added ')
                return render(request,'admin/product_variation.html',{'form':form,'x':x,'y':y,'variation':variation,'variation_category':variation_category,'product_name':product_name})
            else:
                form.save()
                messages.success(request,'product variation added successfully')
                return render(request,'admin/product_variation.html',{'x':x,'y':y})
        else:
            print(form.errors)
            return render(request,'admin/product_variation.html',{'form':form,'x':x,'y':y,'variation_category':variation_category,'product_name':product_name})
    return render(request,'admin/product_variation.html',{'form':form,'x':x,'y':y})


def view_variation(request,id):
    x=Product.objects.get(id=id)
    y=Variation.objects.filter(product=x)
    return render(request,'admin/view_variation.html',{'y':y})


def variation_delete(request,id):
    variation = Variation.objects.get(id=id)
    product= Product.objects.get(id=variation.product_id)
    current_site=get_current_site(request)
    id = product.id
    print(id)
    variation.delete()
    messages.success(request,'Product variation deleted successfully')
    return redirect("http://"+f'{current_site}'+"staff/view_variation/"+f'{id}')



def add_product_gallery(request):
    form=Product_gallery_Form()
    y=Product.objects.all().order_by('-created_date')
    x=ProductGallery.objects.all()
    if request.method=="POST":
        form= Product_gallery_Form(request.POST,request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request,'Product gallery added successfully')
            return render(request,'admin/product_gallery.html',{'form':form,'x':x,'y':y})
        else:
            print(form.errors)
            return render(request,'admin/product_gallery.html',{'form':form,'x':x,'y':y})
    return render(request,'admin/product_gallery.html',{'form':form,'x':x,'y':y})

def customer_queries(request):

    customer = Customer_care.objects.filter(is_solve=False)
    return render(request,'admin/customer_care.html',{'customer':customer})

def customer_queries_solution(request,id):
    customer=Customer_care.objects.get(id=id)
    form=Customer_solution_Form()
    if request.method == "POST":
        customer=Customer_care.objects.get(id=id)
        form= Customer_solution_Form(request.POST)
        subject= request.POST.get('subject')
        print(subject)
        if form.is_valid():
            solution= request.POST.get('solutiom')
            x=form.save()
            x.customer=customer
            x.save()
            customer.is_solve=True
            customer.save()
            mail_subject = 'solution  of your queries'
            message = render_to_string('admin/email_customer.html', {
            'user': request.user,
            'customer':customer,
            'solution':solution,
          
            })
            
            send_email = EmailMessage(mail_subject, message, to=[customer.email])
            # send_email.send()
            customer.is_solve=True
            customer.save()
            messages.success(request,'Sent to mail succesfully')
            return redirect('customer_queries')
        else:
            return render(request,'admin/solution_queries.html',{"customer":customer,'form':form})

    return render(request,'admin/solution_queries.html',{"customer":customer})


def product_disable(request,id):
    product=Product.objects.get(id=id)
    product.status=False
    product.save()
    return redirect('add_product')

def product_enable(request,id):
    product=Product.objects.get(id=id)
    product.status=True
    product.save()
    return redirect('add_product')


def category_delete(request,id):
    product=Category.objects.get(id=id)
    product.delete()
    return redirect('add_category')


def productgallery_delete(request,id):
    product=ProductGallery.objects.get(id=id)
    id=product.product_id
    current_site=get_current_site(request)
    product.delete()
    return redirect("http://"+f'{current_site}'+"staff/view_gallery/"+f'{id}')


def product_variation_disable(request,id):
    variation=Variation.objects.get(id=id)
    variation.status=False
    variation.save()
    return redirect('add_product_variation')

def product_variation_enable(request,id):
    variation=Variation.objects.get(id=id)
    variation.status=True
    variation.save()
    return redirect('add_product_variation')


def add_supplier(request):
    form=Supplier_Form()
    x=Supplier.objects.all()
    if request.method=="POST":
        x=Supplier.objects.all()

        form= Supplier_Form(request.POST,request.FILES) 

        email=request.POST.get('email')
        x=User.objects.filter(email=email).exists()
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        if form.is_valid():
                
            if x:
                error= "Email id already exists"
                messages.error(request,"this email id already exists")
                return render(request,'admin/supplier.html',{'form':form,'x':x,'error':error})
            else:
              
                form.save()
                user=User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email,phone_number=phone_number,roll="supplier")
                password=f'{username}'+"@123"
                user.set_password(password)
                user.is_active=True
                user.save()

                mail_subject = 'Password for your registration !'
                message = render_to_string('admin/password_email.html', {
                'password': password,
                'user':user,
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                # send_email.send()
                messages.success(request,"your login credentials are sent to ypur mail and supplier added successfully")
            
                
                
                return redirect('add_supplier')
         
        else:
            print(form.errors)
            return render(request,'admin/supplier.html',{'x':x,'form':form})
    
    return render(request,'admin/supplier.html',{'form':form})


def view_supplier(request):
     x=Supplier.objects.all().order_by('-created_date')
     return render(request,'admin/view_supplier.html',{'x':x})

def edit_supplier(request,id=None):
    form= Supplier_Form()
    supplier=Supplier.objects.get(id=id)
    id=supplier.id
    user=User.objects.get(email=supplier.email)
    current_site=get_current_site(request)
    print(current_site)
    if request.method=="POST":
        supplier=Supplier.objects.get(id=id)
        user=User.objects.get(email=supplier.email)
        x=Supplier.objects.all()
        form= Supplier_Form(request.POST,request.FILES,instance=supplier) 
        email=request.POST.get('email')
        x=User.objects.filter(email=email).exists()
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        phone_number=request.POST.get('phone_number')
        business_name=request.POST.get('business_name')
        address_lin1=request.POST.get('address_lin1')
        address_lin2=request.POST.get('address_lin2')
        city=request.POST.get('city')
        district=request.POST.get('district')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        if form.is_valid():
                # supplier.first_name= first_name
                # supplier.last_name= last_name
                # supplier.username= username
                # supplier.email= first_name
                # supplier.business_name= business_name
                # supplier.phone_number= first_name
                # supplier.address_lin1= address_lin1
                # supplier.address_lin2= address_lin2
                # supplier.city= city
                # supplier.district= district
                # supplier.state= state
                # supplier.pincode= pincode
                # supplier.country= country
                form.save()
                # user=User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email,phone_number=phone_number,roll="supplier")
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.phone_number=phone_number
                user.roll="supplier"

                password=f'{user.username}'+"@123"
                user.set_password(password)
                user.is_active=True
                user.save()

                messages.success(request," Supplier Edit successfully")
                return redirect("http://"+f'{current_site}'+"/staff/edit_supplier/"+f'{id}')
         
        else:
            print(form.errors)
            return render(request,'admin/edit_supplier.html',{'x':x})
    else:    
        return render(request,'admin/edit_supplier.html',{'supplier':supplier})

def view_gallery(request,id):
    product = Product.objects.get(id=id)
    gallery=ProductGallery.objects.filter(product=product)
    return render(request,'admin/view_gallery.html',{'gallery':gallery})
# supplier order detail
def order_detail_supplier(request):
    y=Supplier.objects.all()
    if request.method=="POST":
       supplier=request.POST.get('supplier')
       x=OrderProduct.objects.filter(supplier_id=supplier).order_by('-created_at')
       return render(request,'admin/order_detail.html',{'x':x,'y':y})
    
    return render(request,'admin/order_detail.html',{'y':y})

def order_history_admin(request):
   x=Order.objects.all().order_by('-created_at')
   return render(request,'admin/order_history.html',{'x':x})

def completed_order(request):
   x=Order.objects.filter(is_completed=True).order_by('-created_at')
   return render(request,'admin/order_history.html',{'x':x})


def confirm_order(request):
   x=Order.objects.filter(is_verified=True).order_by('-created_at')
   return render(request,'admin/order_history.html',{'x':x})


def order_history_supplier(request):
   user=request.user
   x=OrderProduct.objects.filter(supplier=user).order_by('-created_at')
   return render(request,'admin/order_history.html',{'x':x})

# admin orderproduct view
def view_ordered_product(request,id):
    order_product=OrderProduct.objects.filter(order_id=id)
    print(order_product)
    if request.method=="POST":
        order_product=OrderProduct.objects.filter(order_id=id).order_by('-created_at')
        print(order_product)

    return render(request,'admin/view_order_product_view.html',{'order_product':order_product})


def view_supplier_order_detail(request):
   user=request.user.email
   print(user)
   supplier=Supplier.objects.get(email=user)
   print(supplier)
   order_product=OrderProduct.objects.filter(supplier=supplier,ordered=True,confirm_order= False).order_by('-created_at')
   return render(request,'admin/supplier_order_product.html',{'order_product':order_product})



def confirm_order_supplier(request,id):
        order_product=OrderProduct.objects.get(id=id)
        order_product.confirm_order=True
        order_product.cancel_order=False
        order_product.save()
        # mail_subject = 'Hii'+ f'{order_product.order.first_name}' + 'your order has been confirmed'
        # message = render_to_string('admin/order_confirm_email.html', {
        # 'user': request.user,
        # 'order_product':order_product
        # })
        # to_email = request.user.email
        # send_email = EmailMessage(mail_subject, message, to=[order_product.order.email])
        # send_email.send()
        return redirect('view_supplier_order_detail')
    
def cancel_order_supplier(request,id):
        order_product=OrderProduct.objects.get(id=id)
        order_product.cancel_order=True
        order_product.confirm_order=False
        order_product.cancel_status= "Cancelled"
        order_product.save()
        mail_subject = 'Hii'+ f'{order_product.order.first_name}' + 'your order has been cancelled'
        message = render_to_string('admin/order_cancel_email.html', {
        'user': request.user,
        'order_product':order_product
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[order_product.order.email])
        # send_email.send()
        return redirect('view_supplier_order_detail')


def supplier_confirm_order_detail(request):
    user=request.user.email
    print(user)
    supplier=Supplier.objects.get(email=user)

    print("v rgve")
    order_product=OrderProduct.objects.filter(confirm_order=True,ordered =True,supplier=supplier).order_by('-created_at')
    return render(request,'admin/confirm_order_supplier.html',{'order_product':order_product})
    
    
        


def verify_order(request,id):
    
    print(id)
    verify_order=OrderProduct.objects.get(id=id)
    
   
    verify_order.is_verified=True
    verify_order.save()
    mail_subject = 'Hii'+ f'{verify_order.order.first_name}' + 'your order has been confirmed'
    message = render_to_string('admin/order_confirm_email.html', {
        'user': request.user,
        'verify_order':verify_order
        })
       
    send_email = EmailMessage(mail_subject, message, to=[verify_order.order.email])
    # send_email.send()
    return redirect("admin_verified_orders")

    
    # return redirect("supplier_confirmed_admin_view")
    # return redirect("http://127.0.0.1:8000/staff/view_ordered_product/"+f'{x}/')

def verified_orders(request):
    verified_orders=OrderProduct.objects.filter(is_verified=True,confirm_order =True)
    context = {
        'verified_orders': verified_orders,
       
    }
    return render(request,'admin/supplier_confirmed_admin_view.html',context)

def assign_to(request,id):
    sales=Salesman.objects.all()
    order=OrderProduct.objects.get(id=id)
    print(order)
   
    
    if request.method=="POST":
        role=request.POST.get("role")
        print(role)
        order.salesman_id=role
        # assign.salesman_id=role
        
        
        order.save()
        # assign.save()
        return redirect('supplier_confirm_order_detail')
    return render(request,"admin/assign_to.html",{'sales':sales})
    
def edit_assign_to(request,id):
        sales=Salesman.objects.all()
        order=OrderProduct.objects.get(id=id)
        rol=order.salesman_id
        guess=Salesman.objects.get(id=rol)
        print(guess.name)
        if request.method=="POST":
            role=request.POST.get("role")
            print(role)
            order.salesman_id=role
            # assign.salesman_id=role
            
            
            order.save()
            # assign.save()
            return redirect('supplier_confirm_order_detail')
        
        
        return render(request,"admin/edit_assign_to.html",{'sales':sales,'guess':guess})




       
       
        
        
       
            
            
            
           
            # assign_to=OrderProduct

       

   

def add_salesman(request):
    user=request.user.email
    salesman=CorporateAgent.objects.get(email=user)
    sale=salesman.id
    print(sale)
    if request.method=="POST":
        form=SalesmanForm(request.POST)
        if form.is_valid():
            x=form.save()
            print(x)
            x.corporateagent_id=sale

            x.save()
            messages.success(request,"Added Successfully")
            return redirect('add_salesman')
        else:
                print(form.errors)
                return render(request,"admin/add_salesman.html", {'form':form})


    else:

        form=SalesmanForm()
        return render(request,"admin/add_salesman.html")
    
def supplier_confirmed_admin_view(request):
    admin_view=OrderProduct.objects.filter(confirm_order=True,ordered =True,is_verified=False).order_by("-created_at")
    return render(request,"admin/supplier_confirmed_admin_view.html",{'admin_view':admin_view})

def supplier_cancelled_admin_view(request):
    cancel_view=OrderProduct.objects.filter(cancel_order=True)
    return render(request,"admin/supplier_cancelled_admin_view.html",{'cancel_view':cancel_view})


def cancel_order(request,id):

    cancel_order=OrderProduct.objects.get(id=id)
    
   
    cancel_order.is_cancelled=True
    cancel_order.save()
    mail_subject = 'Hii'+ f'{cancel_order.order.first_name}' + 'your order has been cancelled'
    message = render_to_string('admin/order_cancel_email.html', {
        'user': request.user,
       
        'cancel_order':cancel_order
        })
    # to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[cancel_order.order.email])
    # send_email.send()
    
    return redirect("supplier_cancelled_admin_view")


def shipping_details(request,id):
    shipments=OrderProduct.objects.get(id=id)
    order=shipments.order_id
    print(order)
    product=shipments.product_id
    print(product)
    
   
    Shipment.objects.create(order_id=order,product_id=product,orderproduct_id=id)
    ship=SupplierShipment.objects.filter(order_id=order,product_id=product,orderproduct_id=id).first()
  
    track_code = hashlib.md5()
    track_code.update(str(shipments.id).encode())
    track_code.digest()
    track_number = str(track_code.hexdigest()[:12].upper())
    shipments.trackID=track_number
    shipments.shipment_id=True
    shipments.is_track=True
    shipments.save()
    ship.trackID=track_number
    ship.save()
    print(track_number)
    x=Shipment.objects.get(order_id=order,product_id=product,orderproduct_id=id)
    x.trackID=track_number
    x.save()
    messages.success(request,'Generated successfully')
    
    return redirect("mainagent_view")

def add_mainagent(request):
    user=request.user.email
    
    supplier=Supplier.objects.get(email=user)
    print(supplier)
    form=MainAgent_Form()
    x=MainAgent.objects.all()
    if request.method=="POST":
        x=MainAgent.objects.all()

        form= MainAgent_Form(request.POST,request.FILES) 


        email=request.POST.get('email')
        y=User.objects.filter(email=email).exists()
        
       
        if y:
            error= "Email id already exists"
            messages.error(request,"This email id already exists")
            return render(request,'admin/add_mainagent.html',{'form':form,'x':x,'error':error})
    
        elif form.is_valid():
                first_name=request.POST.get('first_name')
                last_name=request.POST.get('last_name')
                username=request.POST.get('username')
                email=request.POST.get('email')
                phone_number=request.POST.get('phone_number')
                agent_organization_name=request.POST.get("business_name")
                
                address_line=request.POST.get("address_line")
                
                state=request.POST.get("state")
                district=request.POST.get("district")
                


                MainAgent.objects.create(state=state,district=district,agent_organization_name=agent_organization_name,phone_number=phone_number,email=email,supplier_id=supplier.id)

                user=User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email,phone_number=phone_number,roll="mainagent")
                password=f'{username}'+"@123"
                user.set_password(password)
                user.is_active=True
                user.save()

                mail_subject = 'Password for your registration !'
                message = render_to_string('admin/password_email_mainagent.html', {
                'password': password,
                'user':user,
                
            
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                # send_email.send()
                # messages.success(request,"payment successful")
            
                
                messages.success(request,'Agent added successfully')
                return render(request,'admin/add_mainagent.html',{'x':x})
         
        else:
            print(form.errors)
            return render(request,'admin/add_mainagent.html',{'form':form,'x':x})
    
    return render(request,'admin/add_mainagent.html',{'form':form,'x':x})


def addcorporateagent(request):
    user=request.user.email
    print(user)
    
    mainagent=MainAgent.objects.get(email=user)
    print(mainagent)
    
   
    
    
    if request.method=="POST":
            form= Corporate_Form(request.POST,request.FILES) 
            email=request.POST.get('email')

            x=User.objects.filter(email=email).exists()
            

            if x:
                error= "Email id already exists"
                messages.error(request,"This email id already exists")
                return render(request,'admin/addcorporateagent.html',{'x':x,'error':error})
    
            elif form.is_valid():
                first_name=request.POST.get('first_name')
                last_name=request.POST.get('last_name')
                username=request.POST.get('username')
                email=request.POST.get('email')
                phone_number=request.POST.get('phone_number')
                agent_organization_name=request.POST.get("business_name")
            
                address_line=request.POST.get("address_line")
                state=request.POST.get("state")
                district=request.POST.get("district")


                phone_number=request.POST.get("phone_number")
                email=request.POST.get("email")
                
                CorporateAgent.objects.create(agent_organization_name=agent_organization_name,state=state,district=district,phone_number=phone_number,email=email,mainagent_id=mainagent.id)
                
                
                user=User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email,phone_number=phone_number,roll="subagent")
                password=f'{username}'+"@123"
                user.set_password(password)
                user.is_active=True
                user.save()

                mail_subject = 'Password for your registration !'
                message = render_to_string('admin/password_email_subagent.html', {
                'password': password,
                'user':user,
                
            
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                # send_email.send()
                

                
                messages.success(request,' added successfully')
                return render(request,'admin/addcorporateagent.html',{'x':x})
         
            else:
                print(form.errors)
                return render(request,'admin/addcorporateagent.html',{'form':form,'x':x})
    else:
     form=Corporate_Form()
     return render(request,'admin/addcorporateagent.html',{'form':form})
    


def about_product(request):
    form=About_Product_Form()
    x=Category.objects.all()
    y=Product.objects.filter(is_available =True)
    if request.method=="POST":
        x=Category.objects.all()
        y=Product.objects.filter(is_available =True)
        form= About_Product_Form(request.POST,request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request,'Product description added successfully')
            return render(request,'admin/about_product.html',{'x':x,'y':y})
        else:
            print(form.errors)
            return render(request,'admin/about_product.html',{'form':form,'x':x,'y':y})
    return render(request,'admin/about_product.html',{'x':x,'y':y})



    
def shipment(request,id):
    user=request.user.email
    
    supplier=Supplier.objects.get(email=user).id
    print(supplier)
    state=State.objects.all()
    district=District.objects.all()

    order_product=OrderProduct.objects.filter(confirm_order=True,ordered =True).order_by('-created_at')
    shipments=OrderProduct.objects.get(id=id)
    print(shipments)
    main_agent=MainAgent.objects.filter(supplier_id=supplier)
    
    
    state=shipments.order.state
    district=shipments.order.district
    order=shipments.order_id
    
    user=shipments.user_id
    product=shipments.product_id
    orderproduct=shipments.id
    # main_agent=MainAgent.objects.all()
   

   
   
   
    if request.method=="POST":
        form=SupplierShipmentForm(request.POST)
       
        expected_delivery_date=request.POST.get("expected_delivery_date")
        location_status=request.POST.get("location_status")
        main_agent=request.POST.get("main_agent")
        date=request.POST.get("created_date")
        # state=request.POST.get("state")
        print(state)
        # district=request.POST.get("district")
        # corporateID = request.POST.get("corporateID")
        # print(corporateID)

        
        if form.is_valid():
            x=form.save()
            
            x.product_id=product
            x.order_id=order
            x.user_id=user
            x.orderproduct_id=orderproduct

            x.is_sent=True
            x.state=state
            x.district=district

           
            x.status_method="Shipped by Supplier"
            # x.date=date
            x.save() 
            shipments.is_shipped=True
            shipments.main_agent=main_agent
            shipments.expected_delivery_date=expected_delivery_date
            
            
            shipments.save()
            messages.success(request,"Shpped Successfully")

            return redirect("admin_verified_supplier_orders")
                    
            # messages.success(request,"Added Successfully")
            # return render(request,"admin/confirm_order_supplier.html",{'x':x,'shipments':shipments,'order_product':order_product})
            
        else:
            print(form.errors)
            return render(request,"admin/shipment.html",{'form':form,'shipments':shipments})

    else:
        form=SupplierShipmentForm()
        return render(request,"admin/shipment.html",{'form':form,'main_agent':main_agent,'shipments':shipments,'order_product':order_product})
    
def corporates_shipment(request,id):
    user=request.user.email
    
    mainagent=CorporateAgent.objects.get(email=user).mainagent_id
    print(mainagent)
    
    shipments=OrderProduct.objects.get(id=id)
    corporate_agent=CorporateAgent.objects.filter(mainagent_id=mainagent)
    print(corporate_agent)
    order_product=OrderProduct.objects.filter(confirm_order=True,ordered =True).order_by('-created_at')
    # main_agent=MainAgent.objects.get(ma)
    
    # state=State.objects.all()
    # district=District.objects.all()
    state=shipments.order.state
    district=shipments.order.district
    order=shipments.order_id
    product=shipments.product_id
    
    print(order)
    user=shipments.user_id
    ship=Shipment.objects.get(order_id=order,product_id=product,orderproduct_id=shipments.id)
    shiptrack=ship.trackID
    product=shipments.product_id
    print(shiptrack)
    expected_delivery_date=shipments.expected_delivery_date
    
    
    print(expected_delivery_date)
   
    if request.method=="POST":
        location_status=request.POST.get("location_status")
        print(location_status)
        date=request.POST.get("created_date")
        # state=request.POST.get("state")
        # district=request.POST.get("district")
        corporatesub_agent=request.POST.get("corporatesub_agent")
        print(corporatesub_agent)
        
       
        
        
        # expected_delivery_date=request.POST.get("expected_delivery_date")
        
        SupplierShipment.objects.create(orderproduct_id=shipments.id,corporatesub_agent=corporatesub_agent,state=state,district=district,user_id=user,order_id=order,status_method="Shipped from corporate agent",location_status=location_status,product_id=product,created_date=date,trackID=shiptrack,expected_delivery_date=expected_delivery_date)
        # shipments.is_agent_shipped=True
        # shipments.save()
        shipments.corporatesub_agent=corporatesub_agent
        shipments.save()
                    
        messages.success(request,"Shpped Successfully")
       
        return redirect("corporateagent_view")
            
      

    else:
        print("hiii")
        
        return render(request,"admin/corporate_shipment.html",{'corporate_agent':corporate_agent,'district':district,'state':state,'shipments':shipments,'corporate_agent':corporate_agent,'order_product':order_product})



def mainagent_shipment(request,id):
    user=request.user.email
    main_agent=MainAgent.objects.get(email=user).id
    shipments=OrderProduct.objects.get(id=id)
    corporate_agent=CorporateAgent.objects.filter(mainagent_id=main_agent)
    order_product=OrderProduct.objects.filter(confirm_order=True,ordered =True).order_by('-created_at')
    main_agent=MainAgent.objects.all()
    
    state=shipments.order.state
    district=shipments.order.district


    order=shipments.order_id
    product=shipments.product_id
    
    print(order)
    user=shipments.user_id
    ship=Shipment.objects.get(order_id=order,product_id=product,orderproduct_id=shipments.id)
    shiptrack=ship.trackID
    product=shipments.product_id
    print(shiptrack)
    expected_delivery_date=shipments.expected_delivery_date
    
    
    print(expected_delivery_date)
   
    if request.method=="POST":
        location_status=request.POST.get("location_status")
        print(location_status)
        date=request.POST.get("created_date")
        
        corporatesub_agent=request.POST.get("corporatesub_agent")
        print(corporatesub_agent)
        
       
        
        
        # expected_delivery_date=request.POST.get("expected_delivery_date")
        
        SupplierShipment.objects.create(orderproduct_id=shipments.id,corporatesub_agent=corporatesub_agent,state=state,district=district,user_id=user,order_id=order,status_method="Shipped by mainagent",location_status=location_status,product_id=product,created_date=date,trackID=shiptrack,expected_delivery_date=expected_delivery_date)
        # shipments.is_agent_shipped=True
        # shipments.save()
        shipments.corporatesub_agent=corporatesub_agent
        shipments.save()
        messages.success(request,"Shpped Successfully")
                    
       
        return redirect("mainagent_view")
            
      

    else:
        print("hiii")
        
        return render(request,"admin/mainagent_shipment.html",{'corporate_agent':corporate_agent,'district':district,'state':state,'shipments':shipments,'order_product':order_product})
    
def assigns_to(request,id):
    user=request.user.email
    corporateagent=CorporateAgent.objects.get(email=user).id
    order_product=OrderProduct.objects.filter(confirm_order=True,).order_by('-created_at')
    sales=Salesman.objects.filter(corporateagent_id=corporateagent)
    order=OrderProduct.objects.get(id=id)
    ship=Shipment.objects.get(order_id=order.order_id,product_id=order.product_id,orderproduct_id=order.id)
    shiptrack=ship.trackID
    print("hell")
    
    
    expected_delivery_date=order.expected_delivery_date
    
   
    
    
    order_id=order.order_id
    product_id=order.product_id
   
    if request.method=="POST":
            role=request.POST.get("role")
            print(role)
            print("hiiii")
            date=request.POST.get("created_date")
            print("sending_date")
            print("hiiii")
            
            location_status=request.POST.get("location_status")
            SupplierShipment.objects.create(location_status="Handover to Salesman",orderproduct_id=order.id,expected_delivery_date=expected_delivery_date,user_id=order.user_id,order_id=order.order_id,trackID=shiptrack,product_id=order.product_id,created_date=date,salesman_id=role,status_method="Assigned")
            order.is_sale_assigned=True
            order.save()

            
            
            return redirect("corporateagent_view")
        # assign.save()
            # return render(request,"admin/corporateagent_view.html",{'order_product':order_product})
    

    return render(request,"admin/assign_to.html",{'sales':sales,'order':order})


def uploads_data(request,id):
    view=SupplierShipment.objects.filter(status_method="Assigned").last()  
    order=view.order_id
    product=view.product_id
    id=view.orderproduct_id
    print(id)
    print(order)

    
    # order=SupplierShipment.objects.get(id=id)
    ship=Shipment.objects.get(order_id=order,product_id=product,orderproduct_id=id)
    print(ship)
    shiptrack=ship.trackID
    
    
    # product=order.product_id
    # order=order.order_id

    # user=request.user.email
    
    # salesman=Salesman.objects.filter(email=user)
    # print(salesman)
    
    
    
   
    order_product=OrderProduct.objects.get(order_id=order,product_id=product)
    print(order_product)
    user_id=order_product.user_id
    
    sales=SupplierShipment.objects.filter(order_id=order,product_id=product,orderproduct_id=id).last()
    sal=sales.salesman_id
    
    


    if request.method=="POST":
        
        
        
        delivered_date=request.POST.get("delivered_date")
        upload_data=request.FILES["upload_data"]
        # upload_data=request.FILES("upload_data")
        print(upload_data)

            
       
                
        SupplierShipment.objects.create(orderproduct_id=id,salesman_id=sal,user_id=user_id,created_date=delivered_date,order_id=order,product_id=product,upload_data=upload_data,delivered_date=delivered_date,is_delivered=True,trackID=shiptrack,status_method="Delivered",location_status="Delivered")
        order_product.status_method="Delivered"
        order_product.delivered_date=delivered_date
        order_product.save()
        return redirect(corporateagent_view)
        
            
        # return render(request,"admin/salesman_view.html",{'view':view,'order_product':order_product})
         
    else: 
        return render(request,"admin/upload_data.html")  
    

# def salesman_view(request):
    
#     view=SupplierShipment.objects.filter(status_method="Assigned") 
#     print(view)
   

#     return render(request,"admin/salesman_view.html",{'view':view})

def track_details(request,id):
    product=OrderProduct.objects.get(id=id)
    track=SupplierShipment.objects.filter(orderproduct_id=product.id,product_id=product.product_id,order_id=product.order_id,trackID=product.trackID)
    return render(request,"admin/track_details.html",{'track':track})


def add_state(request):
    if request.method=="POST":
        state=request.POST.get("state")
        State.objects.create(state=state)
        messages.success(request," Added successfully")

        return render(request,"admin/add_state.html")


    return render(request,"admin/add_state.html")
   

def add_district(request):
    if request.method=="POST":
        district=request.POST.get("district")
        District.objects.create(district=district)
        messages.success(request," Added successfully")

        return render(request,"admin/add_district.html")


    return render(request,"admin/add_district.html")


def mainagent_view(request):
      user=request.user.email
      print("hiii")
      x=MainAgent.objects.get(email=user)
      print(x)
      name=x.agent_organization_name
      print(name)
      view=OrderProduct.objects.filter(main_agent=name).order_by("-created_at")
      print(view)
      return render(request,"admin/mainagent_view.html",{'view':view})


def corporateagent_view(request):
        user=request.user.email
        x=CorporateAgent.objects.get(email=user)
        name=x.agent_organization_name
        view=OrderProduct.objects.filter(corporatesub_agent=name).order_by("-created_at")
        print(view)
        return render(request,"admin/corporateagent_view.html",{'view':view})

def view_added_mainagent(request):
    user=request.user.email
    supplier=Supplier.objects.get(email=user)
    print(user)
    
    view=MainAgent.objects.filter(supplier_id=supplier.id)
    print(view)
    return render(request,"admin/view_added_mainagent.html",{'view':view})

def edit_mainagent(request,id):
    edit=MainAgent.objects.get(id=id)
    form=MainAgent_Form(instance=edit)
    
    if request.method=="POST":
        form=MainAgent_Form(request.POST,instance=edit)
        if form.is_valid():
            edit=form.save()
            edit.save()
            messages.success(request," Edited successfully")

            return redirect('view_added_mainagent')
        else:
            print(form.errors)
            return render(request,"admin/edit_added_mainagent.html",{'edit':edit,'form':form})
    else:
        
        return render(request,"admin/edit_added_mainagent.html",{'edit':edit,'form':form})
   


def delete_mainagent(request,id):
    delete=MainAgent.objects.get(id=id)
    delete.delete()
    messages.success(request," Deleted successfully")

    return redirect("view_added_mainagent")
    
def view_added_corporateagent(request):
    user=request.user.email 
    mainagent=MainAgent.objects.get(email=user)
    view=CorporateAgent.objects.filter(mainagent_id=mainagent.id)
    return render(request,"admin/view_added_corporateagent.html",{'view':view})

def edit_corporateagent(request,id):
    edit=CorporateAgent.objects.get(id=id)
    form=Corporate_Form(instance=edit)
    
    if request.method=="POST":
        form=Corporate_Form(request.POST,instance=edit)
        if form.is_valid():
            edit=form.save()
            edit.save()
            messages.success(request," Edited successfully")

            return redirect('view_added_corporateagent')
        else:
            print(form.errors)
            return render(request,"admin/edit_added_corporateagent.html",{'edit':edit,'form':form})
    else:
        
        return render(request,"admin/edit_added_corporateagent.html",{'edit':edit,'form':form})
   


def delete_corporateagent(request,id):
    delete=CorporateAgent.objects.get(id=id)
    delete.delete()
    messages.success(request," Deleted successfully")

    return redirect("view_added_corporateagent")

def view_added_salesman(request):
    user=request.user.email
    corporateagent=CorporateAgent.objects.get(email=user)  
    
    view=Salesman.objects.filter(corporateagent_id=corporateagent.id)
    print(view)
    return render(request,"admin/view_added_salesman.html",{'view':view})


def edit_salesman(request,id):
    edit=Salesman.objects.get(id=id)
    form=SalesmanForm(instance=edit)
    
    if request.method=="POST":
        form=SalesmanForm(request.POST,instance=edit)
        if form.is_valid():
            edit=form.save()
            edit.save()
            messages.success(request," Edited successfully")

            return redirect('view_added_salesman')
        else:
            print(form.errors)
            return render(request,"admin/edit_added_salesman.html",{'edit':edit,'form':form})
    else:
        
        return render(request,"admin/edit_added_salesman.html",{'edit':edit,'form':form})
   


def delete_salesman(request,id):
    delete=Salesman.objects.get(id=id)
    delete.delete()
    messages.success(request," Deleted successfully")
    return redirect("view_added_salesman")


def admin_return_request(request):
    order = Return.objects.filter(return_status="return_requested")
    return_obj = Return.objects.filter(return_status="refunded",admin_return_status="refunded")
    return render(request,"admin/admin_return_request.html",{'order':order,'return_obj':return_obj})

def admin_return_verify(request,id):
    return_obj = Return.objects.get(id=id)
    return_obj.admin_return_status = "return_requested"
    return_obj.save()
    return redirect('admin_return_request')
    
    # return render(request,"admin/admin_return_request.html",{'return_obj':return_obj})

def supplier_return_request(request):
    user=request.user.email
    supplier=Supplier.objects.get(email=user).id

 
    order = Return.objects.filter(return_status="return_requested", order__supplier__id = supplier, admin_return_status = "return_requested" )
    return_obj = Return.objects.filter(return_status="return_confirmed",order__supplier__id = supplier, admin_return_status = "return_confirmed")
    return render(request,"admin/supplier_return_request.html",{'order':order,'return_obj':return_obj})

def supplier_return_confirm(request,id):
    return_obj=Return.objects.get(id=id)
    return_obj.admin_return_status = "return_confirmed"
    return_obj.return_status = "return_confirmed"
    order=OrderProduct.objects.get(id=return_obj.order_id)
    order.return_status = "return_confirmed"
    order.save()
    return_obj.save()
    return redirect('supplier_return_request')



def  return_complete_supplier(request):
    user=request.user.email
    print(user)
    supplier=Supplier.objects.get(email=user).id
    print(supplier)
    return_ob = Return.objects.filter(return_status="return_complete",order__supplier__id = supplier, admin_return_status = "return_complete")
    return render(request,"admin/return_complete_supplier.html",{'return_ob':return_ob})


def supplier_return_complete(request,id):
    return_obj=Return.objects.get(id=id)
    return_obj.admin_return_status = "return_complete"
    return_obj.return_status = "return_complete"
    order=OrderProduct.objects.get(id=return_obj.order_id)
    order.return_status = "return_complete"
    order.save()
    return_obj.save()
    return redirect('return_complete_supplier')



def supplier_refund_initiate(request,id):
    return_obj=Return.objects.get(id=id)
    return_obj.admin_return_status = "refund_initiated"
    return_obj.return_status = "refund_initiated"
    order=OrderProduct.objects.get(id=return_obj.order_id)
    order.return_status = "refund_initiated"
    order.save()
    return_obj.save()
    return redirect('refund_initiate_supplier')


def  refund_initiate_supplier(request):
    user=request.user.email
    supplier=Supplier.objects.get(email=user).id
    return_ob = Return.objects.filter(return_status="refund_initiated",order__supplier__id = supplier, admin_return_status = "refund_initiated")
    return render(request,"admin/refund_initiate_supplier.html",{'return_ob':return_ob})




def supplier_refund_complete(request,id):
    print('gjhf')
    return_obj=Return.objects.get(id=id)
    return_obj.admin_return_status = "refunded"
    return_obj.return_status = "refunded"
    order=OrderProduct.objects.get(id=return_obj.order_id)
    order.return_status = "refunded"
    order.save()
    return_obj.save()
    return redirect('return_refund_complete')


def  return_refund_complete(request):
    user=request.user.email
    supplier=Supplier.objects.get(email=user).id
    return_ob = Return.objects.filter(return_status="refunded",order__supplier__id = supplier, admin_return_status = "refunded")
    return render(request,"admin/refund.html",{'return_ob':return_ob})


def cancel_requested_orders(request):
    cancel_request=OrderProduct.objects.filter(cancel_status="Cancellation_requested")|OrderProduct.objects.filter(cancel_status="Cancelled").order_by('-created_at')
    return render(request,"admin/cancel_requested_orders.html",{'cancel_request':cancel_request})

def cancelled_order(request,id):
    cancel_order=OrderProduct.objects.get(id=id)
    print(cancel_order)
    cancel_order.cancel_request_admin="Cancellation_requested_from_admin"
    
    cancel_order.save()

    return redirect("cancel_requested_orders")

def cancel_request_from_admin(request):
    cancel_request_admin=OrderProduct.objects.filter(cancel_request_admin="Cancellation_requested_from_admin").order_by('-created_at')
    return render(request,"admin/cancel_request_from_admin.html",{'cancel_request_admin':cancel_request_admin})

def supplier_cancel(request,id):
    supplier_cancel=OrderProduct.objects.get(id=id)
    supplier_cancel.cancel_status="Cancelled"
    mail_subject = 'Hii'+ f'{supplier_cancel.order.first_name}' + 'your order has been cancelled'
    message = render_to_string('admin/order_supplier_cancel_email.html', {
        'user': request.user,
       
        'order_product':supplier_cancel
        })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[supplier_cancel.order.email])
    # send_email.send()
    supplier_cancel.save()
    return redirect("cancel_request_from_admin")


def admin_verified_orders(request):
    admin_verified_order=OrderProduct.objects.filter(is_verified=True,confirm_order=True,ordered=True).order_by("-created_at")
    return render(request,"admin/admin_verified_orders.html",{'admin_verified_order':admin_verified_order})

def admin_verified_supplier_orders(request):
    user=request.user.email
    supplier=Supplier.objects.get(email=user)
    admin_verified_order=OrderProduct.objects.filter(is_verified=True,ordered=True,supplier_id=supplier.id,confirm_order=True).order_by('-created_at')
    return render(request,"admin/admin_verified_supplier_orders.html",{'admin_verified_order':admin_verified_order})












