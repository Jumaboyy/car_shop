from django.shortcuts import render, redirect
from .models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import CartAuthenticatedUser
from django.http import HttpRequest
from . import models
from django.urls import reverse
import stripe
from django.conf import settings
# Create your views here.

def index(request): # Categoriya va productlarni ko'rsatadi asosiy sahifada
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-id')
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'index.html', context)


def shop_detail(request, id):# Bu funksiya mahsulot tafsilotlarini ko'rish uchun ishlatiladi
    product = Product.objects.get(id=id)
    return render(request, 'shop_detail.html', {'product': product})


def shop(request, ):# Bu funksiya barcha mahsulotlarni ko'rsatadi.
    product = Product.objects.all()
    return render(request, 'shop.html', {'products': product})


def product_by_category(request, category_id):# productlarni categoriyalar bo'yicha filtrlaydi
    categories = Category.objects.all()
    products = Product.objects.filter(category=category_id)
    return render(request, 'index.html', {
        'products_category': products,
        'categories': categories
    })


def cart(request): #Bu funksiya foydalanuvchining savatini ko'rsatadi
    cart_info = CartAuthenticatedUser(request).get_cart_info()
    context = {
        'order_products': cart_info['order_products'],
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity']
    }
    return render(request, 'shop_cart.html', context)


def to_cart(request: HttpRequest, product_id, action): # Bu funksiya mahsulotlarni savatga qo'shish
    if request.user.is_authenticated:                  # yoki olib tashlash uchun ishlatiladi.
        CartAuthenticatedUser(request, product_id, action)#
        current_page = request.META.get('HTTP_REFERER')
        return redirect(current_page)

    return redirect('register')


def clear_cart(request): # Bu funksiya savatni tozalash uchun ishlatiladi.
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        order = cart_info['order']
        order_products = order.orderproduct_set.all()
        for order_product in order_products:
            product = order_product.product
            product.quantity += order_product.quantity
            product.save()
            order_product.delete()
        return redirect('cart')
    else:
        return redirect('register')


def login_view(request): # Bu funksiya foydalanuvchini tizimga kirish uchun ishlatiladi.
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')
    return render(request, 'login.html')


def register_view(request): # Bu funksiya yangi foydalanuvchini ro'yxatdan o'tkazish uchun ishlatiladi.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password_conf = request.POST['password2']
        if password == password_conf:
            User.objects.create_user(username=username, password=password)

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Account created successfully')

                return redirect('index')
        else:
            messages.error(request, 'Passwords do not match or are empty')
    return render(request, 'register.html')


def log_out(request): # Bu funksiya foydalanuvchini tizimdan chiqarish uchun ishlatiladi.
    logout(request)
    return redirect('index')


def detele_cart(request, id):  # Bu funksiya savatdan mahsulotni olib tashlash uchun ishlatiladi.
    product_cart = models.OrderProduct.objects.get(id=id)
    product_cart.delete()
    return redirect('cart')


def create_checkout_sessions(request): # Bu funksiya Stripe orqali to'lov seansini yaratish uchun ishlatiladi.
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Auto-Shop'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)



def success_payment(request): # Bu funksiya muvaffaqiyatli to'lovdan so'ng sahifani ko'rsatish uchun ishlatiladi.
    return render(request, 'seccess.html')
