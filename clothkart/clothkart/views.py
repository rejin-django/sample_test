from django.shortcuts import redirect,HttpResponseRedirect,render,HttpResponse
from store.models import Product,ReviewRating,Wishlist
from cart.models import Category
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    products = Product.objects.filter(is_available=True,status=True).order_by('-created_date')
    product=Product.objects.order_by('-created_date').filter(is_available=True,todays_deal=True)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    reviews = None
    saree = Product.objects.order_by('-created_date').filter(Q(description__icontains="saree") | Q(product_name__icontains="saree"))
    # for product in products:
    #     reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    # products = Product.objects.order_by('-created_date').filter(Q(description__icontains="men") | Q(product_name__icontains="Men"))
    # pro=Product.objects.get(slug="black-saree")
    # print(pro)
    context = {
        
        'reviews': reviews,
        'products': paged_products,
        'product_count': product_count,
        'product': product,
        # 'pro':pro,
        'saree':saree,
    }
    return render(request, 'home.html', context)

def men_cloth(request):
    products = Product.objects.order_by('-created_date').filter(Q(description__icontains="shirt") | Q(product_name__icontains="saree"))
    if request.method =="POST":
        products = Product.objects.order_by('-created_date').filter(Q(description__icontains="shirt") | Q(product_name__icontains="saree"))
        context = {
            'products': products,
        }
        return render(request, 'store/store.html', context)
    else:
        return render(request, 'store/store.html', {'products':products})

def watch(request):

    products = Product.objects.order_by('-created_date').filter(Q(description__icontains="watch") | Q(product_name__icontains="watch"))
    if request.method =="POST":
        products = Product.objects.order_by('-created_date').filter(Q(description__icontains="watch") | Q(product_name__icontains="watch"))
        context = {
            'products': products,
        }
        return render(request, 'store/store.html', context)

    return render(request, 'store/store.html', {'products':products})

def view_tv(request):
    products = Product.objects.order_by('-created_date').filter(Q(description__icontains="slipper") | Q(product_name__icontains="shoe"))
    return render(request, 'store/store.html', {'products':products})

def todays_deal(request):
    product=Product.objects.order_by('-created_date').filter(is_available=True,todays_deal=True)
    return render(request, 'store/home.html', {'product':product})

