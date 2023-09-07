from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from addcart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages

# Create your views here.
def place_order(request, total=0, quantity=0,):
    current_user = request.user

    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    address=Order.objects.filter(user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.district = form.cleaned_data['district']

            data.pincode = form.cleaned_data['pincode']

            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

        else:
            context = {
                'form':form,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'address':address
            }
            return render(request,'store/checkout.html',context)


    else:
        return redirect('checkout')



def payment(request,id):
    order=Order.objects.get(id=id)
    if request.method=="POST":
        order=Order.objects.get(id=id)
        payment_id=order.order_number
        payment_method=request.POST.get('payment_method')
        print(payment_method)
        amount_paid=order.order_total
        payment=Payment.objects.create(user=order.user,payment_id=payment_id, payment_method=payment_method,amount_paid=amount_paid,status="completed")
        order.payment_id=payment
        order.status="Confirmed"
        order.is_ordered=True
        order.save()
        cart_item=CartItem.objects.filter(user=request.user)
        for item in cart_item:
            orderproduct = OrderProduct()
            orderproduct.order_id=order.id
            orderproduct.payment=payment
            orderproduct.user_id = request.user.id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.tax= (float(item.product.price) * 2)/100
            orderproduct.total_price= float(orderproduct.product_price) + float(orderproduct.tax)
            orderproduct.product_id = item.product_id
            orderproduct.ordered = True
            orderproduct.is_order=True

            orderproduct.supplier_id = item.product.supplier.id
            orderproduct.cancel_status="New"
            orderproduct.save()
            cart_items = CartItem.objects.get(id=item.id)
            product_variation = cart_items.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()
        ordered_products = OrderProduct.objects.filter(order_id=order.id,is_order=True,cancel_status="New")
        subtotal = 0
        for i in ordered_products:
             subtotal += i.product_price * i.quantity
        CartItem.objects.filter(user=request.user).delete()
        # mail_subject = 'Thank you for your order!'
        # message = render_to_string('orders/order_recieved_email.html', {
        # 'user': request.user,
        # 'order': order,
        # 'cart_item':cart_item
        # })
        # to_email = request.user.email
        # send_email = EmailMessage(mail_subject, message, to=[to_email])
        # send_email.send()
        
        return render(request, 'orders/order_complete.html',{'order':order,'cart_item':cart_item,'subtotal':subtotal,'ordered_products':ordered_products})
    else:
        return render(request,'orders/pay.html')

def order(request):
    return render(request,'orders/order.html')

def order_complete(request):
    order= Order.objects.get(user=request.user,is_ordered=True)
    order_number=order.order_number
    transID=order.payment_id
    # order_number = request.GET.get('order_number')
    # transID = request.GET.get('payment_id')
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    print(ordered_products)

    subtotal = 0
    for i in ordered_products:
        subtotal += i.product_price * i.quantity

    payment = Payment.objects.get(user=request.user)

    context = {
        'order': order,
        'ordered_products': ordered_products,
        'order_number': order.order_number,
        'transID': order.payment_id,
        'payment': payment,
        'subtotal': subtotal,
    }
    return render(request, 'orders/order_complete.html', context)


