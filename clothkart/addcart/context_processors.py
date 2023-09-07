from .models import Cart, CartItem
from .views import _cart_id
import datetime

from dateutil import relativedelta

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)


# def notification(request):
#     date=datetime.datetime.now()
#     allnotifications = BroadcastNotification.objects.all()
#     notify=[]
#     for i in allnotifications:
#         x=i.broadcast_on
#         diff=relativedelta.relativedelta(date,x)
#         if diff.years > 0 or diff.months > 0 or diff.days > 0 or diff.minutes > 0 or diff.seconds > 0 :
#             notify.append(i)
#     y=len(notify)
#     t=len(allnotifications)
#     no=t-y
#     print(y)
#     print(notify)
#     return dict(notification=notify,no=no)
 