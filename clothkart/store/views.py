from django.shortcuts import render,get_object_or_404,redirect
from.forms import Product_Form
from.models import Product,ReviewRating,ProductGallery,Wishlist,About_Product
from cart.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from addcart.models import Cart,CartItem
from addcart.views import _cart_id
from django.db.models import Q
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from datetime import date,timedelta



# Create your views here.
def addproduct(request):
    form=Product_Form()
    if request.method=="POST":
        form=Product_Form(*request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'includes/addproduct.html',{'form':form})

    return render(request,'store/addproduct.html',{'form':form})

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True,status=True).order_by('-created_date')
        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        shoe=Product.objects.filter(category_id = "11",is_available=True,status=True).order_by('-id')
        slipper=Product.objects.filter(category_id = "4",is_available=True,status=True).order_by('-id')
        today = date.today()
        print(today)
        delivery=today+timedelta(days=20)
    else:
        products = Product.objects.all().filter(is_available=True,status=True).order_by('-id')
        paginator = Paginator(products, 60)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        shoe=Product.objects.filter(category_id = "11",is_available=True,status=True).order_by('-id')
        slipper=Product.objects.filter(category_id = "4",is_available=True,status=True).order_by('-id')
        today = date.today()
        print(today)
        delivery=today+timedelta(days=20)
        

    context = {
        'products': paged_products,
        'product_count': product_count,
        'shoe':shoe,
        'slipper':slipper,
        'delivery':delivery,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        cat_product = Product.objects.filter(Q(category__slug=category_slug) | Q(slug=product_slug)|Q(description__icontains="shirt") | Q(product_name__icontains="saree") | Q(description__icontains="dress") | Q(description__icontains="slipper") | Q(description__icontains="shoe") | Q(description__icontains="cloth"))
 
        about_product=About_Product.objects.filter(product_id=single_product.id)
        today = date.today()
        print(today)
        delivery=today+timedelta(days=20)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    # if request.user.is_authenticated:
    #     try:
    #         orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    #     except OrderProduct.DoesNotExist:
    #         orderproduct = None
    # else:
    #     orderproduct = None

    # # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    if request.user.is_authenticated:
       wishlist= Wishlist.objects.filter(product_id=single_product.id,user=request.user,wishlist=True).first()
    else:
        wishlist=None
    # # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    
     
    context = {
        'single_product': single_product,
        'cat_product' :cat_product,
        'in_cart'       : in_cart,
        'wishlist': wishlist,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'delivery':delivery,
        'about_product':about_product,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):


    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
            context = {
                'products': products,
                'product_count': product_count,
            }
            return render(request, 'store/store.html', context)
        else:
           return render(request, 'store/store.html') 

    # if 'keyword' in request.GET:
    #     keyword = request.GET['keyword']
    #     if keyword:
    #         products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    #         product_count = products.count()
    # context = {
    #     'products': products,
    #     'product_count': product_count,
    # }
    # return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        print('hi')
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def wishlist(request):
    user=request.user
    products=Wishlist.objects.filter(user=user,wishlist=True)
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    return render(request, 'store/wishlist.html',{'products':paged_products})



def add_wishlist(request,product_id):
    product=Product.objects.get(id=product_id)
    wish=Wishlist.objects.filter(product=product,user=request.user,wishlist=True).first()
    if wish:
         wish.wishlist=False
         wish.save()
         return redirect('wishlist')
    else:
       wishlist=Wishlist.objects.create(product=product,user=request.user,wishlist=True)
       return redirect('wishlist')
    



# def cart(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass 

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax'       : tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/cart.html', context)
